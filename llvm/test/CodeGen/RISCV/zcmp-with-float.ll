; NOTE: Assertions have been autogenerated by utils/update_llc_test_checks.py UTC_ARGS: --version 2
; RUN: llc -mtriple=riscv32 -mattr=+f,+zcmp -target-abi ilp32f -verify-machineinstrs < %s | FileCheck %s --check-prefix=RV32
; RUN: llc -mtriple=riscv64 -mattr=+f,+zcmp -target-abi lp64f -verify-machineinstrs < %s | FileCheck %s --check-prefix=RV64

declare void @callee()

; Test the file could be compiled successfully.
; .cfi_offset of fs0 is wrong here. It should be fixed by #66613.
define float @foo(float %arg) {
; RV32-LABEL: foo:
; RV32:       # %bb.0: # %entry
; RV32-NEXT:    cm.push {ra}, -32
; RV32-NEXT:    .cfi_def_cfa_offset 32
; RV32-NEXT:    fsw fs0, 12(sp) # 4-byte Folded Spill
; RV32-NEXT:    .cfi_offset ra, -4
; RV32-NEXT:    .cfi_offset fs0, -4
; RV32-NEXT:    fmv.s fs0, fa0
; RV32-NEXT:    call callee@plt
; RV32-NEXT:    fmv.s fa0, fs0
; RV32-NEXT:    flw fs0, 12(sp) # 4-byte Folded Reload
; RV32-NEXT:    cm.popret {ra}, 32
;
; RV64-LABEL: foo:
; RV64:       # %bb.0: # %entry
; RV64-NEXT:    cm.push {ra}, -32
; RV64-NEXT:    .cfi_def_cfa_offset 32
; RV64-NEXT:    fsw fs0, 12(sp) # 4-byte Folded Spill
; RV64-NEXT:    .cfi_offset ra, -8
; RV64-NEXT:    .cfi_offset fs0, -4
; RV64-NEXT:    fmv.s fs0, fa0
; RV64-NEXT:    call callee@plt
; RV64-NEXT:    fmv.s fa0, fs0
; RV64-NEXT:    flw fs0, 12(sp) # 4-byte Folded Reload
; RV64-NEXT:    cm.popret {ra}, 32
entry:
  call void @callee()
  ret float %arg
}