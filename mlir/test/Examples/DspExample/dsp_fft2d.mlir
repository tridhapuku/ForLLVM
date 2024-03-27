// func.func @test_static_rfft2d(%arg0: tensor<5x5x8xf32>) -> (tensor<5x5x5xf32>, tensor<5x5x5xf32>) {
//   %output_real, %output_imag = "tosa.rfft2d"(%arg0) {} : (tensor<5x5x8xf32>) -> (tensor<5x5x5xf32>, tensor<5x5x5xf32>)
//   return %output_real, %output_imag : tensor<5x5x5xf32>, tensor<5x5x5xf32>
// }


func.func @test_fft2d(%arg0: tensor<1x4x8xf32>, %arg1: tensor<1x4x8xf32>) -> (tensor<1x4x8xf32>, tensor<1x4x8xf32>) {
  %0, %1 = tosa.fft2d %arg0, %arg1 {inverse = false} : (tensor<1x4x8xf32>, tensor<1x4x8xf32>) -> (tensor<1x4x8xf32>, tensor<1x4x8xf32>)
  return %0, %1 : tensor<1x4x8xf32>, tensor<1x4x8xf32>
}

// func.func @const_test() -> (tensor<i32>) {
//   // CHECK: [[C3:%.+]] = arith.constant dense<3> : tensor<i32>
//   %result = "tosa.const"() {value = dense<3> : tensor<i32>} : () -> tensor<i32>

// //   // CHECK: return [[C3]]
//   return %result : tensor<i32>
// }

// ./mlir-opt fft_help.mlir --pass-pipeline="builtin.module(func.func(tosa-to-linalg))"


// ./mlir-opt fft_help.mlir --pass-pipeline="builtin.module(func.func(tosa-to-linalg-named,tosa-to-linalg,tosa-to-tensor, tosa-to-arith, convert-arith-to-llvm), arith-bufferize, arith-expand, memref-expand, convert-arith-to-llvm, convert-func-to-llvm)" 


// WORKS 
// ./mlir-opt fft_help.mlir --pass-pipeline="builtin.module(func.func(tosa-to-linalg,tosa-to-arith, tosa-to-linalg-named, convert-linalg-to-affine-loops, lower-affine, tosa-to-scf, convert-scf-to-cf, arith-expand, convert-arith-to-llvm, canonicalize, llvm-legalize-for-export, bufferization-bufferize, convert-bufferization-to-memref, finalizing-bufferize  ),one-shot-bufferize,func-bufferize, convert-cf-to-llvm, convert-func-to-llvm, finalize-memref-to-llvm)" -o sample_llvm.mlir 


// WORKS 2

// ./mlir-opt fft_help.mlir --pass-pipeline="builtin.module(func.func(tosa-to-linalg-named,tosa-to-arith, tosa-to-linalg, convert-linalg-to-affine-loops, lower-affine, tosa-to-scf, convert-scf-to-cf, arith-expand, convert-arith-to-llvm, canonicalize, llvm-legalize-for-export,empty-tensor-to-alloc-tensor, buffer-hoisting, buffer-loop-hoisting, buffer-deallocation),drop-equivalent-buffer-results, func-bufferize, convert-cf-to-llvm, convert-func-to-llvm, finalize-memref-to-llvm)" --opaque-pointers=0 --mlir-print-ir-before-all

// -o sample2_llvm.mlir

// - --empty-tensor-to-alloc-tensor

/// before drop one-shot-bufferize{bufferize-function-boundaries}
