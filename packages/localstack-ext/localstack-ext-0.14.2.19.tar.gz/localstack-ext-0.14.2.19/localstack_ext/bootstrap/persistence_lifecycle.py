import os
import localstack.config as localstack_config
from localstack.utils.files import cp_r
from localstack.utils.objects import SubtypesInstanceManager
from localstack.utils.testutil import create_zip_file
import localstack_ext.config as ext_config
class PersistenceLifeCycle(SubtypesInstanceManager):
 def assets_root(self)->str:
  raise NotImplementedError()
 def get_assets_location(self)->str:
  base_path=(localstack_config.dirs.data if ext_config.PERSIST_ALL else localstack_config.dirs.tmp)
  return os.path.join(base_path,self.assets_root())
 def retrieve_assets(self)->bytes:
  return create_zip_file(self.get_assets_location(),get_content=True)
 def inject_assets(self,pod_assets_dir:str):
  current_assets=self.get_assets_location()
  pod_assets=os.path.join(pod_assets_dir,self.assets_root())
  cp_r(pod_assets,current_assets)
 def on_after_reset(self):
  pass
 @classmethod
 def get_base_type(cls):
  return PersistenceLifeCycle
# Created by pyminifier (https://github.com/liftoff/pyminifier)
