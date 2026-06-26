# Performance

Performance does not really matter often in the beginning, but it might start mattering a lot and actually be a question of is it feasible or not to do something, when scaling the sample up.
Most of performance optimization should be the high impact levers at first, before tackling some small things if it is actually worth it.
High impact levers include: using a compiled language, parallelization across CPU cores or even using a GPU, getting rid of unnecessary disk writes and memory accesses and just writing more efficient algorithms in the parts where they matter most.
You should not start optimizing for performance before it is actually needed or known to be needed.

## By default, do not optimize

Most often, you can make your code faster by optimizing, but even quicker would be to just run your code instead of improving it.
For many research applications, it is more important that the code is correct, clear and reproducible.
You should first measure run times, before optimizing at all.

## Highest optimization levers

### Python vs C / Rust

Python is an interpreted language, meaning that the code is converted into machine readable form at run time, not before. This is in stark contrast to C, which is compiled first, and run then.
The advantage of this is that the CPU does not have the overhead of converting code to machine readable form, and thus C and Rust are way faster, but also more complex to write.

### Data storage

Most often bottlenecks occur with memory access and disk writes. Reading and writing to RAM is expensive, and slow, and very often the bottleneck. Disk writes are even slower. Thus, you should keep an eye on your program's disk operations: it could be that most of the time the CPU is just waiting for data to be transported from the disk or RAM.
There, a well working approach could be to use a properly optimized database, which reads or preloads into memory the data that is needed. For RAM optimization, one can improve memory access patterns (the same thing might be possible with fewer reads), like reading from an array tends to have values stored in memory next to eachother, allowing the cpu to prefetch future array members.

### Branches

On modern CPU's, each of them have some form of branch prediction. This means that for every if-else statement in the code, the CPU tries to predict which path will be taken, and executes that path in advance for greater speed.
The cost of the branch prediction are branch prediction misses, where the prediction is wrong, and the program execution slows down. This can be mitigated by reducing number of branches as well as having the if-else structure be rather "if valid/common case, do this, else rare case" rather than "if invalid/rare case, do this, else do common path". Some languages have the ability to do branch prediction hints.

### Parallelization

There are three main levels of parallelization: instruction level parallelism, vectorization and thread-level parallelism.
Vectorization, coarsely, means that the CPU performs operations on vectors of 4 or 8 numbers at a time, at the same speed it would take to do the same operation for a single number. This requires some preprocessing to "feed" vectors to the CPU. Instruction level parallelism means the CPU takes multiple instructions at the same time for execution, instead of only one instruction per clock cycle. Threads or multiple core parallelism exploit the fact that in modern CPUs, we have at least 4 cores that we can use at the same time, executing the work in parallel, instead of only having one core (the default) doing work at a time.

Most often, with C, you can have the compiler to do automatic vectorization and instruction level parallelism. 
Thread-level parallelism is what requires more attention from you. There, you will need to tell the computer how many cores to use at each part, and how to partition the work between different CPU cores.
The difference between threads and cores is that threads are virtual cores, quicker to create, and they help to keep the CPU core busy, like different waiters bringing work to one chef to ensure that the chef is not sitting idle at any time.

Even with these, most of the time optimizing, is actually spent understanding memory access patterns and improving those. The bottleneck is very often how quickly we can get data to the CPU to be processed, and not necessarily the calculation "power" of the CPU.

In recent years, there has been a rise of GPGPUs, graphics processing units used for general processing. GPUs are massively parallel: they have more transistors dedicated to simpler cores, and thus, instead of 8 or 16 cores, they might easily have 10 000 "cuda cores", organized differently than CPU cores. GPUs also have soldered memory, which allows for increased memory bandwidth, but the caveat is that the data has to be first transferred from main system memory to the GPU VRAM for this bandwidth to be exploited, and that transfer process is not quick.

You can write code to be run on a GPU with a couple specialized programming languages, like OpenCL (for all GPUs), Cuda (Nvidia GPUs), Bend, and in the future, hopefully other better languages. Cuda and OpenCL are quite laborious to write, and it often takes some work to even get the code to run faster than a CPU baseline version. Most often, in a research pipeline, you should only run a specific portion that A) takes long and B) is an embarrassingly parallel problem on the GPU. But, well optimized GPU code for a well suited problem, can yield big improvements. A workstation GPU like the RTX 5080 can theoretically achieve around 56 teraflop (trillions of floating point operations like multiply or add etc.) per second, versus a workstation CPU like Ryzen 9 9950x can achieve around 5.4 teraflop/s at the same accuracy.

## General principles

When optimizing, you should always measure first, and only then start tackling any optimizations. The biggest levers will be the technologies and architecture that you are using, not small optimizations.

The above was a short, condensed intro to optimization. If you are more interested in the topic, I recommend going through the Aalto course [Programming parallel computers](https://ppc.cs.aalto.fi/). The material is open year round, with good exercises as well as explanations on what we touched. moi
