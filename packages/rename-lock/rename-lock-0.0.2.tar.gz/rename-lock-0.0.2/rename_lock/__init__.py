
# Easy file exclusive locking tool [rename_lock]

import os
import sys
import fies
import time
from sout import sout

# 名称変更のトライアルループ
def rename_loop(filename, post_filename, retry_interval):
	while True:
		try:
			# 変更の試行
			os.rename(filename, post_filename)
			# 成功時
			return True
		except:
			time.sleep(retry_interval)

# ロックオブジェクト
class RLockObj:
	# 初期化処理
	def __init__(self, org_filename, post_filename):
		# 変更後ファイル名
		self.filename = post_filename
		# 元のファイル名
		self.org_filename = org_filename
	# ロック解除
	def unlock(self):
		# 名称変更によるロック解除
		os.rename(self.filename, self.org_filename)
	# with構文突入時
	def __enter__(self):
		return self	# 自身を返す (with構文の簡易的な使い方)
	# with構文脱出時
	def __exit__(self, ex_type, ex_value, trace):
		# ロック解除
		self.unlock()

# ロックオブジェクト生成
def rename_lock(filename, retry_interval = 0.01):
	# 名称変更後のファイル名
	post_filename = "%s.locked"%filename
	# 名称変更のトライアルループ
	rename_loop(filename, post_filename, retry_interval)
	# ロックオブジェクト
	rlock = RLockObj(filename, post_filename)
	return rlock

# 呼び出しの準備
sys.modules[__name__] = rename_lock	# モジュールオブジェクトとrename_lock関数を同一視
