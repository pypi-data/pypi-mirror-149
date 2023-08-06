
from setuptools import setup
# 公開用パッケージの作成 [ezpip]
import ezpip

# 公開用パッケージの作成 [ezpip]
with ezpip.packager(develop_dir = "./_develop_rename_lock/") as p:
	setup(
		name = "rename-lock",
		version = "0.0.0",
		description = "Easy file exclusive locking tool based on file rename",
		author = "bib_inf",
		author_email = "contact.bibinf@gmail.com",
		url = "https://github.co.jp/",
		packages = p.packages,
		install_requires = ["ezpip", "sout"],
		long_description = p.long_description,
		long_description_content_type = "text/markdown",
		license = "CC0 v1.0",
		classifiers = [
			"Programming Language :: Python :: 3",
			"License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
		],
	)
