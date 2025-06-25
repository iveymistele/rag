1. Create data on the CPU.

2. Send data from the CPU to the GPU (for DL this is done in batches).

3. Compute result on the GPU.

4. Send the result back to the CPU.

Depending on the DL framework/LLM pipeline you are using, some of these steps may be automatically done for you.

