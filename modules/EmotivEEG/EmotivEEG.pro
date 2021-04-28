TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

INCLUDEPATH += ./include

QMAKE_CXXFLAGS +=-std=c++1y
QMAKE_LFLAGS   +=-std=c++1y

SOURCES += \
        main.cpp \
    arguments.cpp \
    emotiveeg.cpp \
    test.cpp \
    research.cpp

HEADERS += \
    arguments.h \
    test.h \
    research.h

LIBS += -ldl
win32:CONFIG(release, debug|release): LIBS += -ledk
else:win32:CONFIG(debug, debug|release): LIBS += -ledk
else:unix: LIBS += -ledk
