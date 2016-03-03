import luigi
import os

class BottomTask(luigi.Task):
	dirname=luigi.Parameter()
	def run(self):
		os.system("mkdir "+self.dirname)
	def output(self):
		return None
	def requires(self):
		return None
	def complete(self):
		return 1
	
class MiddleTask(luigi.Task):
	filename=luigi.Parameter()
	dirname=luigi.Parameter()
	filecontents=luigi.Parameter()

	def requires(self):
		#return BottomTask(self.dirname)
		return None

	def run(self):
		os.system("mkdir "+self.dirname)
		os.system("echo '"+self.filecontents+"' >"+self.dirname+"/"+self.filename)

	def complete(self):
		return 1

class TopTask(luigi.Task):
	filename=luigi.Parameter()
	dirname=luigi.Parameter()
	filecontents=luigi.Parameter()
	
	def requires(self):
		return MiddleTask(self.filename, self.dirname, self.filecontents)
	
	def run(self):
		os.system("cat "+self.dirname+"/"+self.filename)
