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
      file.write("#! /bin/bash\n#SBATCH -N 1\n#SBATCH --ntasks-per-node="+cpu+
                 "\n#SBATCH --gres=gpu:A100-SXM4:"+gpu+"\n#SBATCH --time="+time+
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
  def vasp(self,command,parallel_run,root):
    count=0
    self.bash=0
    file=open("bash"+str(bash)+".sh","w")
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
        file=open("bash"+str(bash)+".sh","w")
        file.write("#!/bin/bash\n")
        file.write("cd "+root+"\n")
        file.write("cd "+i+"\n")
        file.write(command+"\n")
        file.write("cd .. \n")
    file.close()
