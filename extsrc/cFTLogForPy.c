/* cFTLogForPy.c */

#include "cFTLogForPy.h"

/////////////////////////////////////////////////////////////////////
// GLOBALS
/////////////////////////////////////////////////////////////////////
int logNdx;                         // 0-based current index
int secondThreadStarted = false;    // SHOULD NOT NEED ?

cLogDesc_t* logDescs[CLOG_MAX_LOG];             

/////////////////////////////////////////////////////////////////////
// OBJECT-LEVEL CODE 
/////////////////////////////////////////////////////////////////////

typedef struct {
    PyObject_HEAD
    // this indexes logDescs, which contains logDir and logName
    long objNdx;            // long to be consistent with Python
    // maybe more later
} LogForPyObject;

// a forward declaration of sorts
static PyTypeObject LogForPyType;

/* LogForPy new() ------------------------------------------------ */
static LogForPyObject *
newLogForPyObject(void)
{
    return (LogForPyObject *)PyObject_New(LogForPyObject, &LogForPyType);
}

/* LogForPy dealloc() -------------------------------------------- */
static void
LogForPy_dealloc(PyObject *ptr)
{
    PyObject_Del(ptr);
}

/* LogForPy __init__ ---------------------------------------------- */
PyDoc_STRVAR(LogForPy_init__doc__,
"Initialize log object.");

static PyObject *
LogForPy_init(LogForPyObject *self, PyObject *args) {
    char* pathToLog;
    if (!PyArg_ParseTuple(args, "s", &pathToLog))
        return NULL;
    int objNdx = _openCLog(pathToLog);
    if (objNdx < 0) {
        return NULL;
    }
    self->objNdx = objNdx;
    Py_INCREF(Py_None);             // XXX ???
    return Py_None;
}

/* count --------------------------------------------------------- */
PyDoc_STRVAR(LogForPy_getCount__doc__,       "Get log message count.");

static PyObject *
LogForPy_getCount(LogForPyObject* self) {
    int ndx     = (int) self->objNdx;
    // XXX SHOULD LOCK
    long count  = (long) logDescs[ndx]->count;
    // XXX AND UNLOCK
    return PyInt_FromLong(count);
}
/* ndx ----------------------------------------------------------- */
PyDoc_STRVAR(LogForPy_getNdx__doc__,       "Get objNdx attr.");

static PyObject *
LogForPy_getNdx(LogForPyObject* self) {
    return PyInt_FromLong(self->objNdx);
}
/* logFile ----------------------------------------------------------- */
PyDoc_STRVAR(LogForPy_getPathToLog__doc__,       "Get path to log file.");

static PyObject *
LogForPy_getPathToLog(LogForPyObject* self) {
    int ndx         = (int)self->objNdx;
    cLogDesc_t* p   = logDescs[ndx];
    char s[MAX_PATH_LEN+1];
    strncpy(s, p->logDir, MAX_PATH_LEN+1);
    int x = strlen(s);
    if (x < MAX_PATH_LEN) {
        strcat (s, "/");
        x = strlen(s);
        if (x < MAX_PATH_LEN) {
            int bytesLeft = MAX_PATH_LEN - x;
            strncat(s, p->logName, bytesLeft+1);
        }
    }
    return PyString_FromString(s);
}


/* logMsg -------------------------------------------------------- */
PyDoc_STRVAR(LogForPy_logMsg__doc__,       "Write a log message.");

static PyObject* 
LogForPy_logMsg(LogForPyObject* self, PyObject* args) {
    int     ndx = (int)self->objNdx;
    const   char* msg;

    if (!PyArg_ParseTuple(args, "s", &msg))
        return NULL;
    if (msg)
        _logMsg(ndx, msg);
    Py_RETURN_NONE;
}

/* LogForPy object methods --------------------------------------- */
static PyMethodDef LogForPy_methods[] = {
    {"init",    (PyCFunction)LogForPy_init,     
                METH_VARARGS,   LogForPy_init__doc__},
    {"count",   (PyCFunction)LogForPy_getCount, 
                METH_NOARGS,    LogForPy_getCount__doc__},
    {"logFile", (PyCFunction)LogForPy_getPathToLog, 
                METH_NOARGS,    LogForPy_getPathToLog__doc__},
    {"logMsg",  (PyCFunction)LogForPy_logMsg,   
                METH_VARARGS,   LogForPy_logMsg__doc__},
    {"ndx",     (PyCFunction)LogForPy_getNdx,   
                METH_NOARGS,    LogForPy_getNdx__doc__},
    {NULL,        NULL}         /* sentinel */
};

static PyGetSetDef LogForPy_getseters[] = {
    {NULL}  /* Sentinel */
};


static PyMemberDef LogForPy_members[] = {
    {NULL}  /* Sentinel */
};


/* without the next line LogForPyType becomes an int */
static PyTypeObject 
LogForPyType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "cFTLogForPy.cFTLogForPy",  /*tp_name*/
    sizeof(LogForPyObject), /*tp_size*/
    0,                      /*tp_itemsize*/
    /* methods */
    LogForPy_dealloc,       /*tp_dealloc*/
    0,                      /*tp_print*/
    0,                      /*tp_getattr*/
    0,                      /*tp_setattr*/
    0,                      /*tp_compare*/
    0,                      /*tp_repr*/
    0,                      /*tp_as_number*/
    0,                      /*tp_as_sequence*/
    0,                      /*tp_as_mapping*/
    0,                      /*tp_hash*/
    0,                      /*tp_call*/
    0,                      /*tp_str*/
    0,                      /*tp_getattro*/
    0,                      /*tp_setattro*/
    0,                      /*tp_as_buffer*/
    /* XXX ADD BASE FLAG */
    Py_TPFLAGS_DEFAULT,     /*tp_flags*/
    0,                      /*tp_doc*/
    0,                      /*tp_traverse*/
    0,                      /*tp_clear*/
    0,                      /*tp_richcompare*/
    0,                      /*tp_weaklistoffset*/
    0,                      /*tp_iter*/
    0,                      /*tp_iternext*/
    LogForPy_methods,       /* tp_methods */
    LogForPy_members,       /* tp_members */
    LogForPy_getseters,     /* tp_getset */
};

/////////////////////////////////////////////////////////////////////
// MODULE-LEVEL CODE 
/////////////////////////////////////////////////////////////////////

/* MODULE METHODS -------------------------------------- */
PyDoc_STRVAR(LogForPy_new__doc__,
"Return a new LogForPy object.");

static PyObject *
LogForPy_new(PyObject *self, PyObject *args, PyObject *kwdict)
{
    LogForPyObject *new;

    if ((new = newLogForPyObject()) == NULL)
        return NULL;

    if (PyErr_Occurred()) {
        Py_DECREF(new);
        return NULL;
    }

    return (PyObject *)new;
}

// the method table - other methods referred to are defined in modFunc.c

static PyMethodDef CLogForPyMethods[] = {
    // METH_VARARGS means that the arguments are passed as a tuple
    // which will be parsed with PyArg_ParseTuple()
    {"initCLogger",     initCLogger,    METH_VARARGS,
        "init data structures, start background thread"},
    {"openCLog",     openCLog,    METH_VARARGS,
        "open named log file"},
    {"logMsg",          logMsg,         METH_VARARGS,
        "write a message to the log"},
    {"closeCLogger",    closeCLogger,   METH_VARARGS,
        "stop background thread, join, close log file"},

    /* DEFINED IN THIS FILE, ABOVE --------------------- */
    {"LogForPy", (PyCFunction)LogForPy_new, METH_VARARGS|METH_KEYWORDS, 
        LogForPy_new__doc__},
    {NULL, NULL, 0, NULL}       /* sentinel = end of this list */
};

/* MODULE INITIALIZATION  ---------------------------------------- */

/* the method name MUST be "init" prefixed to the module name */

PyMODINIT_FUNC
initcFTLogForPy(void) {
    PyObject *m;
    Py_TYPE(&LogForPyType) = &PyType_Type;          // cant
    if (PyType_Ready(&LogForPyType) < 0)
        return;

    // this used to be cast to void; there should be a third, dquoted
    // parameter, a description
    m = Py_InitModule("cFTLogForPy", CLogForPyMethods);
    
    if (m == NULL) {
        return;
    }
    // XXX ADD A CONSTANT, JUST FOR FUN
    PyModule_AddIntConstant(m, "max_log", CLOG_MAX_LOG);
}

// XXX EVERYTHING IN THIS FUNCTION MUST ALSO BE IN THE VERSION ABOVE 
// PyMODINIT_FUNC
// OTHER_initcFTLogForPy(void)
// {
//     PyObject *m;
// 
//     Py_TYPE(&LogForPyType) = &PyType_Type;
//     if (PyType_Ready(&LogForPyType) < 0) {
//         return;
//     }
//     m = Py_InitModule("cFTLogForPy", LogForPy_functions);
//     if (m == NULL) {
//         return;
//     }
// }  
