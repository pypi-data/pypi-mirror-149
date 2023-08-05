/**
 * Copyright 2015 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Ensure that Python.h is included before any other header.
#include "common.h"

#include "bytecode_breakpoint.h"

#include "bytecode_manipulator.h"
#include "python_callback.h"
#include "python_util.h"

namespace devtools {

/**
 * We copy paste the functions inside linetable namespace from CPython. (They should've export these symbols but they don't)
 * Until CPython does export the relevant symbols - when upgrading to new python, you should manually check that these
 * functions haven't changed, and bump the minor version in the check below.
 */
#if PY_VERSION_HEX >= 0x030B0000
#error "Unsupported Python version. Please make sure that PyLineTable* functions haven't changed"
#endif
#if PY_VERSION_HEX >= 0x030A0000
    namespace linetable {

        void
        PyLineTable_InitAddressRange(const char *linetable, Py_ssize_t length, int firstlineno, PyCodeAddressRange *range)
        {
            range->opaque.lo_next = linetable;
            range->opaque.limit = range->opaque.lo_next + length;
            range->ar_start = -1;
            range->ar_end = 0;
            range->opaque.computed_line = firstlineno;
            range->ar_line = -1;
        }

        static void
        retreat(PyCodeAddressRange *bounds)
        {
            int ldelta = ((signed char *)bounds->opaque.lo_next)[-1];
            if (ldelta == -128) {
                ldelta = 0;
            }
            bounds->opaque.computed_line -= ldelta;
            bounds->opaque.lo_next -= 2;
            bounds->ar_end = bounds->ar_start;
            bounds->ar_start -= ((unsigned char *)bounds->opaque.lo_next)[-2];
            ldelta = ((signed char *)bounds->opaque.lo_next)[-1];
            if (ldelta == -128) {
                bounds->ar_line = -1;
            }
            else {
                bounds->ar_line = bounds->opaque.computed_line;
            }
        }

        static void
        advance(PyCodeAddressRange *bounds)
        {
            bounds->ar_start = bounds->ar_end;
            int delta = ((unsigned char *)bounds->opaque.lo_next)[0];
            bounds->ar_end += delta;
            int ldelta = ((signed char *)bounds->opaque.lo_next)[1];
            bounds->opaque.lo_next += 2;
            if (ldelta == -128) {
                bounds->ar_line = -1;
            }
            else {
                bounds->opaque.computed_line += ldelta;
                bounds->ar_line = bounds->opaque.computed_line;
            }
        }

        static inline int
        at_end(PyCodeAddressRange *bounds) {
            return bounds->opaque.lo_next >= bounds->opaque.limit;
        }

        int
        PyLineTable_PreviousAddressRange(PyCodeAddressRange *range)
        {
            if (range->ar_start <= 0) {
                return 0;
            }
            retreat(range);
            while (range->ar_start == range->ar_end) {
                assert(range->ar_start > 0);
                retreat(range);
            }
            return 1;
        }

        int
        PyLineTable_NextAddressRange(PyCodeAddressRange *range)
        {
            if (at_end(range)) {
                return 0;
            }
            advance(range);
            while (range->ar_start == range->ar_end) {
                assert(!at_end(range));
                advance(range);
            }
            return 1;
        }
    }
#endif // PY_VERSION_HEX >= 0x030A0000
namespace cdbg {

// Each method in python has a tuple with all the constants instructions use.
// Breakpoint patching appends more constants. If the index of new constant
// exceed 0xFFFF, breakpoint patching would need to use extended instructions,
// which is not supported. We therefore limit to methods with up to 0xF000
// instructions that leaves us with up to 0x0FFF breakpoints.
static const int kMaxCodeObjectConsts = 0xF000;

BytecodeBreakpoint::BytecodeBreakpoint()
    : cookie_counter_(1000000) {
}


BytecodeBreakpoint::~BytecodeBreakpoint() {
  Detach();
}


void BytecodeBreakpoint::Detach() {
  for (auto it = patches_.begin(); it != patches_.end(); ++it) {
    it->second->breakpoints.clear();
    PatchCodeObject(it->second);

    // TODO(vlif): assert zombie_refs.empty() after garbage collection
    // for zombie refs is implemented.

    delete it->second;
  }

  patches_.clear();

  for (auto it = cookie_map_.begin(); it != cookie_map_.end(); ++it) {
    delete it->second;
  }

  cookie_map_.clear();
}


int BytecodeBreakpoint::SetBreakpoint(
    PyCodeObject* code_object,
    int line,
    PyObject* hit_callback,
    std::function<void()> error_callback)
{

  CodeObjectBreakpoints* code_object_breakpoints =
      PreparePatchCodeObject(ScopedPyCodeObject::NewReference(code_object));
  if (code_object_breakpoints == nullptr) {
    error_callback();
    return -1;  // Not a valid cookie, but "ClearBreakpoint" wouldn't mind.
  }

  // Find the offset of the instruction at "line". We use original line
  // table in case "code_object" is already patched with another breakpoint.
#if PY_VERSION_HEX >= 0x030A0000
  PyCodeAddressRange range;
  const char *linetable = PyBytes_AS_STRING(code_object->co_linetable);
  Py_ssize_t length = PyBytes_GET_SIZE(code_object->co_linetable);
  linetable::PyLineTable_InitAddressRange(linetable, length, code_object->co_firstlineno, &range);
  while (range.ar_line != line) {
          if (!linetable::PyLineTable_NextAddressRange(&range)) {
#else
  CodeObjectLinesEnumerator lines_enumerator(
      code_object->co_firstlineno,
      code_object_breakpoints->original_lnotab.get());
  while (lines_enumerator.line_number() != line) {
    if (!lines_enumerator.Next()) {
#endif
      LOG(ERROR) << "Line " << line << " not found in "
                 << CodeObjectDebugString(code_object);
      error_callback();
      return -1;
    }
  }

  // Assign cookie to this breakpoint and Register it.
  const int cookie = cookie_counter_++;

  std::unique_ptr<Breakpoint> breakpoint(new Breakpoint);
  breakpoint->code_object = ScopedPyCodeObject::NewReference(code_object);
  breakpoint->line = line;
#if PY_VERSION_HEX >= 0x030A0000
  breakpoint->offset = range.ar_start;
#else
  breakpoint->offset = lines_enumerator.offset();
#endif

  breakpoint->hit_callable = hit_callback;
  breakpoint->error_callback = error_callback;
  breakpoint->cookie = cookie;

  code_object_breakpoints->breakpoints.insert(
      std::make_pair(breakpoint->offset, breakpoint.get()));

  DCHECK(cookie_map_[cookie] == nullptr);
  cookie_map_[cookie] = breakpoint.release();

  PatchCodeObject(code_object_breakpoints);

  return cookie;
}


void BytecodeBreakpoint::ClearBreakpoint(int cookie) {
  auto it_breakpoint = cookie_map_.find(cookie);
  if (it_breakpoint == cookie_map_.end()) {
    return;  // No breakpoint with this cookie.
  }

  // Previously, hit_callable d id not refer to the user's callback directly --
  // but to a callback generated by this extension, which the extension would use to
  // disable the breakpoint here - so that even if the existing bytecode is used after disabling
  // (e.g. in the case of a long-running function),
  // the breakpoint would immediately stop being hit.
  // This has been replaced with functionality implemented in google_bdb._callback in order to allow
  // the modified bytecode to be pickled (for Spark support).

  auto it_code = patches_.find(it_breakpoint->second->code_object);
  if (it_code != patches_.end()) {
    CodeObjectBreakpoints* code = it_code->second;

    auto it = code->breakpoints.begin();
    int erase_count = 0;
    while (it != code->breakpoints.end()) {
      if (it->second == it_breakpoint->second) {
        code->breakpoints.erase(it);
        ++erase_count;
        it = code->breakpoints.begin();
      } else {
        ++it;
      }
    }

    DCHECK_EQ(1, erase_count);

    PatchCodeObject(code);

    if (code->breakpoints.empty() && code->zombie_refs.empty()) {
      delete it_code->second;
      patches_.erase(it_code);
    }
  } else {
    DCHECK(false) << "Missing code object";
  }

  delete it_breakpoint->second;
  cookie_map_.erase(it_breakpoint);
}


BytecodeBreakpoint::CodeObjectBreakpoints*
BytecodeBreakpoint::PreparePatchCodeObject(
    const ScopedPyCodeObject& code_object) {
  if (code_object.is_null() || !PyCode_Check(code_object.get())) {
    LOG(ERROR) << "Bad code_object argument";
    return nullptr;
  }

  auto it = patches_.find(code_object);
  if (it != patches_.end()) {
    return it->second;  // Already loaded.
  }

  std::unique_ptr<CodeObjectBreakpoints> data(new CodeObjectBreakpoints);
  data->code_object = code_object;
  data->original_stacksize = code_object.get()->co_stacksize;

  data->original_consts =
      ScopedPyObject::NewReference(code_object.get()->co_consts);
  if ((data->original_consts == nullptr) ||
      !PyTuple_CheckExact(data->original_consts.get())) {
    LOG(ERROR) << "Code object has null or corrupted constants tuple";
    return nullptr;
  }

  if (PyTuple_GET_SIZE(data->original_consts.get()) >= kMaxCodeObjectConsts) {
    LOG(ERROR) << "Code objects with more than "
               << kMaxCodeObjectConsts << " constants not supported";
    return nullptr;
  }

  data->original_code =
      ScopedPyObject::NewReference(code_object.get()->co_code);
  if ((data->original_code == nullptr) ||
      !PyBytes_CheckExact(data->original_code.get())) {
    LOG(ERROR) << "Code object has no code";
    return nullptr;  // Probably a built-in method or uninitialized code object.
  }


#if PY_VERSION_HEX >= 0x030A0000
  data->original_lnotab =
      ScopedPyObject::NewReference(code_object.get()->co_linetable);
#else
    data->original_lnotab =
      ScopedPyObject::NewReference(code_object.get()->co_lnotab);
#endif

  patches_[code_object] = data.get();
  return data.release();
}


void BytecodeBreakpoint::PatchCodeObject(CodeObjectBreakpoints* code) {
  PyCodeObject* code_object = code->code_object.get();

  if (code->breakpoints.empty()) {
    code->zombie_refs.push_back(ScopedPyObject(code_object->co_consts));
    code_object->co_consts = code->original_consts.get();
    Py_INCREF(code_object->co_consts);

    code_object->co_stacksize = code->original_stacksize;

    code->zombie_refs.push_back(ScopedPyObject(code_object->co_code));
    code_object->co_code = code->original_code.get();
    VLOG(1) << "Code object " << CodeObjectDebugString(code_object)
            << " reverted to " << code_object->co_code
            << " from patched " << code->zombie_refs.back().get();
    Py_INCREF(code_object->co_code);


#if PY_VERSION_HEX >= 0x030A0000
    PyObject* line_table = code_object->co_linetable;
#else
    PyObject* line_table = code_object->co_lnotab;
#endif
    if (line_table != nullptr) {
      code->zombie_refs.push_back(ScopedPyObject(line_table));
    }
    line_table = code->original_lnotab.get();
    Py_INCREF(line_table);

    return;
  }

  std::vector<uint8> bytecode = PyBytesToByteArray(code->original_code.get());

  bool has_lnotab = false;
  std::vector<uint8> lnotab;
  if (!code->original_lnotab.is_null() &&
      PyBytes_CheckExact(code->original_lnotab.get())) {
    has_lnotab = true;
    lnotab = PyBytesToByteArray(code->original_lnotab.get());
  }

  BytecodeManipulator bytecode_manipulator(
      std::move(bytecode),
      has_lnotab,
      std::move(lnotab));

  // Add callbacks to code object constants and patch the bytecode.
  std::vector<PyObject*> callbacks;
  callbacks.reserve(code->breakpoints.size());

  std::vector<std::function<void()>> errors;

  int const_index = PyTuple_GET_SIZE(code->original_consts.get());
  for (auto it_entry = code->breakpoints.begin();
       it_entry != code->breakpoints.end();
       ++it_entry, ++const_index)
  {
    int offset = it_entry->first;
    bool offset_found = true;
    const Breakpoint& breakpoint = *it_entry->second;
    DCHECK_EQ(offset, breakpoint.offset);

    callbacks.push_back(breakpoint.hit_callable);

#if PY_VERSION_HEX >= 0x03060000
      // In Python 3, since we allow upgrading of instructions to use
    // EXTENDED_ARG, the offsets for lines originally calculated might not be
    // accurate, so we need to recalculate them each insertion.
    offset_found = false;
    if (bytecode_manipulator.has_lnotab())
    {
      ScopedPyObject lnotab(PyBytes_FromStringAndSize(
          reinterpret_cast<const char*>(bytecode_manipulator.lnotab().data()),
          bytecode_manipulator.lnotab().size()));

#if PY_VERSION_HEX >= 0x030A0000
      PyCodeAddressRange range;
      const unsigned char *linetable = bytecode_manipulator.lnotab().data();
      Py_ssize_t length = bytecode_manipulator.lnotab().size();
      linetable::PyLineTable_InitAddressRange((const char*)linetable, length, code_object->co_firstlineno, &range);
      while (range.ar_line != breakpoint.line) {
          if (!linetable::PyLineTable_NextAddressRange(&range)) {
            break;
          }
          offset = range.ar_start;
      }
      offset_found = range.ar_line == breakpoint.line;
#else
      CodeObjectLinesEnumerator lines_enumerator(code_object->co_firstlineno,
                                             lnotab.release());
      while (lines_enumerator.line_number() != breakpoint.line) {
      if (!lines_enumerator.Next()) {
          break;
        }
      offset = lines_enumerator.offset();
      }
      offset_found = lines_enumerator.line_number() == breakpoint.line;
#endif // PY_VERSION_HEX >= 0x030A0000
      }
#endif // PY_VERSION_HEX >= 0x03060000



    if (!offset_found ||
        !bytecode_manipulator.InjectMethodCall(offset, const_index)) {
      LOG(WARNING) << "Failed to insert bytecode for breakpoint "
                   << breakpoint.cookie << " at line " << breakpoint.line;
      errors.push_back(breakpoint.error_callback);
    }
  }

  // Create the constants tuple, the new bytecode string and line table.
  code->zombie_refs.push_back(ScopedPyObject(code_object->co_consts));
  ScopedPyObject consts = AppendTuple(code->original_consts.get(), callbacks);
  code_object->co_consts = consts.release();

  code_object->co_stacksize = code->original_stacksize + 1;

  code->zombie_refs.push_back(ScopedPyObject(code_object->co_code));
  ScopedPyObject bytecode_string(PyBytes_FromStringAndSize(
      reinterpret_cast<const char*>(bytecode_manipulator.bytecode().data()),
      bytecode_manipulator.bytecode().size()));
  DCHECK(!bytecode_string.is_null());
  code_object->co_code = bytecode_string.release();
  VLOG(1) << "Code object " << CodeObjectDebugString(code_object)
          << " reassigned to " << code_object->co_code
          << ", original was " << code->original_code.get();

  if (has_lnotab) {
#if PY_VERSION_HEX >= 0x030A0000
    PyObject* line_table = code_object->co_linetable;
#else
    PyObject* line_table = code_object->co_lnotab;
#endif
    code->zombie_refs.push_back(ScopedPyObject(line_table));
    ScopedPyObject lnotab_string(PyBytes_FromStringAndSize(
        reinterpret_cast<const char*>(bytecode_manipulator.lnotab().data()),
        bytecode_manipulator.lnotab().size()));
    DCHECK(!lnotab_string.is_null());
    line_table = lnotab_string.release();
  }

  // Invoke error callback after everything else is done. The callback may
  // decide to remove the breakpoint, which will change "code".
  for (auto it = errors.begin(); it != errors.end(); ++it) {
    (*it)();
  }
}

}  // namespace cdbg
}  // namespace devtools
