
Contents:

    1) What does this code do?

    2) How to build ?
         i)From llvm-project/build directory
            a)cmake -G Ninja ../llvm -DLLVM_ENABLE_PROJECTS=mlir  -DLLVM_BUILD_EXAMPLES=ON -DBUILD_SHARED_LIBS=ON -DLLVM_TARGETS_TO_BUILD="X86" -DCMAKE_BUILD_TYPE=Release -DLLVM_USE_LINKER=lld -DLLVM_OPTIMIZED_TABLEGEN=ON -DLLVM_USE_NEWPM=ON

            -b) ninja

    3) Run with example:
        i) From llvm-project/build directory:
        ninja && ./bin/dsp1 ../mlir/test/Examples/DspExample/dsp_gain_op.py -emit=mlir-affine

        ii) Tosa to LinAlg lowering example, from llvm-project/build directory:
        ninja && ./bin/dsp1 ../mlir/test/Examples/DspExample/dsp_fft2d.mlir -emit=mlir-linalg