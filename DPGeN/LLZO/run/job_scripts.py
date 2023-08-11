class auto_job:
  def __init__(self,jobs,tasks):
    self.jobs=jobs
    self.tasks=tasks
  def init(self,prefix):
    self.folders=[]
    for i in range(self.jobs):
      for j in range(self.tasks[i]):
        self.folders.append(prefix+".00"+str(i)+".*00"+str(j))
  def submit_script(self):
    pass
  def job_script(self,gpu,cpu,time):
    for i in range(self.bash+1):

      file=open(str(i)+".sh","w")
      file.write("#! /bin/bash\n#SBATCH -N 1\n#SBATCH --ntasks-per-node="+str(cpu)+
                 "\n#SBATCH --gres=gpu:A100-SXM4:"+str(gpu)+"\n#SBATCH --time="+time+
                 "\n#SBATCH --error=job.%J.err\n#SBATCH --output=job.%J.out\n")
      file.write('echo "Starting at `date`"\n')
      file.write('echo "Running on hosts: $SLURM_NODELIST"\n')
      file.write('echo "Running on $SLURM_NNODES nodes."\n')
      file.write('echo "Running $SLURM_NTASKS tasks."\n')
      file.write('echo "Job id is $SLURM_JOBID"\n')
      file.write('echo "Job submission directory is : $SLURM_SUBMIT_DIR"\n')
      file.write('cd $SLURM_SUBMIT_DIR\n')
      file.write('##################\n')
      file.write('bash bash'+str(i)+".sh")
      file.close()
  def bash_script(self,command,parallel_run,root):
    count=0
    self.bash=0
    file=open("bash"+str(self.bash)+".sh","w")
    file.write("#!/bin/bash\n")
    for i in self.folders:
      if count < len(self.folders)//parallel_run:
        file.write("cd "+root+"\n")
        file.write("cd "+i+"\n")
        file.write(command+"\n")
        file.write("cd .. \n")
        count+=1
      else:
        file.close()
        count=1
        self.bash+=1
        file=open("bash"+str(self.bash)+".sh","w")
        file.write("#!/bin/bash\n")
        file.write("cd "+root+"\n")
        file.write("cd "+i+"\n")
        file.write(command+"\n")
        file.write("cd .. \n")
    file.close()
#=========================================================
a=auto_job(5,[204,204,204,204,4])
a.init("task")
vasp_command="/opt/nvidia/hpc_sdk/Linux_x86_64/21.7/comm_libs/mpi/bin/mpirun -n 1 /nlsasfs/home/aidevmat/sahebb/software/vasp/vasp_gpu/vasp.6.3.2_test/bin/vasp_std_gpu"
lmp_command="lmp -i input.lammps -v restart 0"
dp_command="/nlsasfs/home/aidevmat/sahebb/software/Miniconda3/envs/dpmd_gpu/bin/dp train input.json "
root="/nlsasfs/home/aidevmat/sahebb/chayan/remote_root/final/lmp/3ff175d196a7a78d43159cdd7d191270a714d9c0"
a.bash_script(lmp_command,12,root)
a.job_script(1,8,"1-00:00:00")

