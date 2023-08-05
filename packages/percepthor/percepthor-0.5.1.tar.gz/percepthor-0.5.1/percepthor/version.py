from cerver.utils.log import LOG_TYPE_NONE, cerver_log_both

from .lib import lib

PERCEPTHOR_VERSION = "0.5.1"
PERCEPTHOR_VERSION_NAME = "Version 0.5.1"
PERCEPTHOR_VERSION_DATE = "03/05/2022"
PERCEPTHOR_VERSION_TIME = "07:56 CST"
PERCEPTHOR_VERSION_AUTHOR = "Erick Salas"

version = {
	"id": PERCEPTHOR_VERSION,
	"name": PERCEPTHOR_VERSION_NAME,
	"date": PERCEPTHOR_VERSION_DATE,
	"time": PERCEPTHOR_VERSION_TIME,
	"author": PERCEPTHOR_VERSION_AUTHOR
}

percepthor_libauth_version_print_full = lib.percepthor_libauth_version_print_full
percepthor_libauth_version_print_version_id = lib.percepthor_libauth_version_print_version_id
percepthor_libauth_version_print_version_name = lib.percepthor_libauth_version_print_version_name

def pypercepthor_version_print_full ():
	output = "\nPyPercepthor Version: {name}\n" \
		"Release Date: {date} - {time}\n" \
		"Author: {author}\n".format (**version)

	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		output.encode ("utf-8")
	)

def pypercepthor_version_print_version_id ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyPercepthor Version ID: {version.id}\n".encode ("utf-8")
	)

def pypercepthor_version_print_version_name ():
	cerver_log_both (
		LOG_TYPE_NONE, LOG_TYPE_NONE,
		f"\nPyPercepthor Version: {version.name}\n".encode ("utf-8")
	)
