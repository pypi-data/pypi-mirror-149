# rename_lock

下の方に日本語の説明があります

## Overview
- Easy file exclusive locking tool based on file rename.

## Usage
- While you are in "WITH" area, the file is locked and cannot be edited by any other process.
- While locked, the file will be renamed to "original_name.locked"
	- The name can be obtained with rlock.filename
```python
with rename_lock("./demo_file.txt") as rlock:
	# operation on locked file
	temp_filename = rlock.filename	# temporary file name
	with open(temp_filename, "w") as f:
		f.write("something")
```
- About Unlocking
	- The lock is automatically unlocked when exiting "WITH" area.
	- Also, when using "WITH", it will automatically unlock when stopped due to an error or when stopped by ctrl+C.
	- However, there may be cases where the file is not unlocked, such as when the entire window is erased.

- The following is how to write when not using "WITH".
```python
rlock = rename_lock("./demo_file.txt")
print(rlock.filename)
rlock.unlock()
```


## 概要
- 手軽なファイルの排他ロックツール
	- ファイルの名称変更を動作原理とする
- 説明は執筆中です

## 使用例
- 下記のように、with内にいる間ファイルの編集がロックされます
- ロック中はファイルは「元の名前.locked」という名前に変更されます
	- その名前はrlock.filenameで取得できます
```python
with rename_lock("./demo_file.txt") as rlock:
	# lockしたファイルに対する操作を書く
	temp_filename = rlock.filename	# temporary file name
	with open(temp_filename, "w") as f:
		f.write("something")
```
- ロック解除について
	- withを抜けると自動的にロック解除されます
	- また、エラーによる停止やctrl+Cによる停止時にも、withを使っている場合は自動的にロック解除されます
	- ただし、ウィンドウごと消した場合など、ロック解除されない場合もあります

- 下記はwithを使わない場合の書き方です
```python
rlock = rename_lock("./demo_file.txt")
print(rlock.filename)
rlock.unlock()
```
