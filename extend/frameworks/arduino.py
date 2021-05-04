from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinomicrochippic32")
BUILD_CORE = env.BoardConfig().get("build.core")
assert isdir(FRAMEWORK_DIR)

env.Append(
    CPPDEFINES=[
        ("ARDUINO", 10808),
        "ARDUINO_ARCH_PIC32",
        ("IDE", "Arduino")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", BUILD_CORE)
    ],

    LIBPATH=[
        join(FRAMEWORK_DIR, "cores", BUILD_CORE),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ],

    LINKFLAGS=[
        join(FRAMEWORK_DIR, "cores", BUILD_CORE, "cpp-startup.S")
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Process USB flags
#

cpp_flags = env.Flatten(env.get("CPPDEFINES", []))
if any(str(f).startswith("PIO_ARDUINO_ENABLE_USB") for f in cpp_flags):
    env.Append(
        CPPDEFINES=[
            "__USB_ENABLED__",
            "__SERIAL_IS_USB__"
        ]
    )
if "PIO_ARDUINO_ENABLE_USB_SERIAL" in cpp_flags:
    env.Append(CPPDEFINES=["__USB_CDCACM__"])
elif "PIO_ARDUINO_ENABLE_USB_HID" in cpp_flags:
    env.Append(CPPDEFINES=["__USB_CDCACM_KM__"])

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants",
                 env.BoardConfig().get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", BUILD_CORE)
))

env.Prepend(LIBS=libs)
