import platform

print('system and bit'.center(40, '-'))
print(platform.architecture(), '\n')

print('system and deatial'.center(40, '-'))
print(platform.platform(), '\n')

print('system'.center(40, '-'))
print(platform.system(), '\n')

print('version'.center(40, '-'))
print(platform.version(), '\n')

print('系统信息'.center(40, '-'))
print(platform.uname(), '\n')

print("python Version".center(40, '-'))
print(platform.python_version(), '\n')

