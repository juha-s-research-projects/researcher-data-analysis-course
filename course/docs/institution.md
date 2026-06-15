# Institutional offerings

This chapter is about what the university has to offer for your research pipeline.
There are a couple offerings that could offer you help: Aalto Datahub, Aalto Triton and the Finance department server.


## Aalto Datahub:

Datahub in a Nutshell: 
1) Consolidates and disseminates several data sources into a single data hub
2) Centralizes data acquisition including vendor negotiation and purchasing
3) Facilitates easy access to commercial and unique, high-quality datasets

Goal: Datahub enables researchers (and students) to increase their productivity by removing data-related obstacles

Access: datahub.aalto.fi
Data sources: https://datahub.aalto.fi/en/data-sources#/

Note: Always check the license, availability, access process, and citation requirements under the data-sources details page

Datahub further allows researchers to promote their data-related research under https://datahub.aalto.fi/en/data-related-research-programs#/. This allows junior and senior researchers to: 
1) Promote their work
2) Make their custom data available to other researchers (good for citations!)
3) Find collaborators on research projects
4) Raise their profile.

## Finance department server

The finance department has a couple servers of its own.
They are maintained by Antti Lehtinen (antti.lehtinen@aalto.fi).
If you want or need access, you can get access and instructions on usage from him.
The servers run a Windows environment with one server being an SQL server, common to the whole department.

### When do you need a larger machine?

You will primarily need a larger machine when the one you typically use runs out of memory or disk space, or has long running jobs that you want to leave to run, instead of babysitting over multiple days.
Typically, it is quite rare to run out of memory with clever programming, but this is still possible.
Disk space is the primary reason to work on the server, as well as long running jobs, and the servers also have way more CPU and network resources and allow collaboration with other people.
I recommend trying to mirror your development environment to be similar to the one on the server, and then deploy the code via git on the server to another machine.

The server access works via a Windows app, which is available at least for Windows machines, as well as MacOS.
That application does not exist on Linux, but there are a couple alternatives that could work, like Remmina, FreeRDP or something else.

The Finance Department server do not have dedicated GPUs, and they are therefore not the place you should run local large language models on, as that is a rather inefficient use of CPU resources, instead, you should go look for Triton.

## Aalto Triton

Aalto Triton is Aalto's own GPU / computing cluster. 
This is the place you should go to if you need specifically GPU type compute resources.
It is maintained by School of Science at Aalto, and the execution model is very different from the Finance department servers.
The Finance department servers provide you a remote GUI so using one is like using a desktop computer normally.
But using Triton, you (typically) ssh into a login node, and then you submit jobs using a program called "slurm" which queues up everybody's jobs.
The larger a job is, the more it needs to wait before it gets processed, and the smaller a job is, the quicker it gets processed.
The jobs are also structured as array jobs, meaning the program (you make) should be able to be called with an array of inputs, and will output an array of outputs.

The learning curve on this machine is higher, but it isn't impossible at all. There is more information here:
https://scicomp.aalto.fi/aalto/welcomeresearchers/ with information about how to apply for an account, how to use the cluster.
There are also courses offered periodically, and a daily garage where you can get help if needed.
