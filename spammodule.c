#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyObject *
spam_hello(PyObject *self, PyObject *args)
{
    puts("Hello");
    Py_RETURN_NONE;
}

static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS, "Execute a shell command."},
    {"hello",  spam_hello, METH_VARARGS, "Print hello to stdout"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* Begin  custom object testing area */

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    char mem[10];
    int  foo;
    int  bar;
} FunProcessor;

static void
Custom_dealloc(FunProcessor *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    FunProcessor *self;
    self = (FunProcessor *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->foo = 0;
	self->bar = 0;
    }
    return (PyObject *) self;
}



static int
Custom_init(FunProcessor *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"foo", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist,
                                     &self->foo))
        return -1;
    return 0;
}


static PyMemberDef Custom_members[] = {
    {"foo", T_INT, offsetof(FunProcessor, foo), 0, "custom number"},
    {NULL}  /* Sentinel */
};

static PyObject *
Custom_quux(FunProcessor *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong(self->bar++);
}

static PyMethodDef Custom_methods[] = {
    {"quux", (PyCFunction) Custom_quux, METH_NOARGS,
     "Returns internal state and bumps it"
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject CustomType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "spam.FunProcessor",
    .tp_doc = "Custom objects",
    .tp_basicsize = sizeof(FunProcessor),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Custom_new,
    .tp_init = (initproc) Custom_init,
    .tp_dealloc = (destructor) Custom_dealloc,
    .tp_members = Custom_members,
    .tp_methods = Custom_methods,
};

/* End    custom object testing area */

/* Begine BF impl */
#define NONE 0
#define LEFT -1
#define RIGHT 1

#define MEMSIZE 4096
#define IOBUFFSIZE 4096
typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    PyObject *code;  // will share a ptr to code string
    unsigned char memory[MEMSIZE];
    unsigned int memptr;
    unsigned int codeptr;
    
    unsigned int stdoutptr;
    unsigned int stdinptr;
    
    char _stdout[IOBUFFSIZE];
    char _stdin[IOBUFFSIZE];

    int bounce_dir;
    int steps_taken;
    u_int brkt_depth;
} CBFI;

static void
CBFI_dealloc(CBFI *self)
{	
    Py_XDECREF(self->code);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
CBFI_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CBFI *self;
    self = (CBFI *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->code = PyUnicode_FromString("");
        if (self->code == NULL) {
            Py_DECREF(self);
            return NULL;
        }

    self->memptr = 0;
    self->codeptr = 0;
    self->stdoutptr = 0;
    self->stdinptr = 0;
    self->bounce_dir = NONE;
    self->steps_taken = 0;
    self->brkt_depth = 0;
    for (int i=0; i<IOBUFFSIZE; i++){
        self->_stdout[i] = 0; self->_stdin[i] = 0;}
    for (int i=0; i<MEMSIZE; i++) {self->memory[i] = 0;}
    }
    return (PyObject *) self;
}

static int
CBFI_init(CBFI *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"mempwr", "stdin", NULL};

    PyObject *stdinlist = NULL;
    PyObject *mempwr = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iO", kwlist,
                                     &mempwr, &stdinlist))
        return -1;
    // TODO: this must ste an error
    if((NULL != stdinlist) && !PyList_Check(stdinlist)) return -1;
    if(stdinlist){
    	Py_ssize_t stdinlen = PyList_Size(stdinlist);
	    // stdin is converted to numbers elsewhere
	    for(int i=0; i<stdinlen; i++){
		    self->_stdin[i] = (char) PyLong_AsLong(PyList_GetItem(stdinlist, i));
    		}
    	}
    return 0;
}

static PyObject *
CBFI_peekmem(CBFI *self, PyObject *Py_UNUSED(ignored))
{
    printf("%hhu %hhu %hhu %hhu %hhu\n",
            self->memory[0], self->memory[1], self->memory[2],
            self->memory[3], self->memory[4]);
    Py_RETURN_NONE;
}

static PyObject *
CBFI_dumpstdout(CBFI *self, PyObject *Py_UNUSED(ignored))
{
    printf("%s\n", self->_stdout);
    Py_RETURN_NONE;
}

static PyObject *
CBFI_getmem(CBFI *self, void *closure)
{
	PyObject *memlist = PyList_New(MEMSIZE);
	for(int i=0; i<MEMSIZE; i++) PyList_SetItem(memlist, i, PyLong_FromLong(self->memory[i]));
	return memlist;
}

static PyObject *
CBFI_setmem(CBFI *self, PyObject *value, void *closure)
{
	puts("Cannot set CBFI memory directly");
	Py_RETURN_NONE;
}

static PyObject *
CBFI_getstdout(CBFI *self, void *closure)
{
	PyObject *stdoutlist = PyUnicode_FromString(self->_stdout);
	return stdoutlist;
}

static PyObject *
CBFI_setstdout(CBFI *self, PyObject *value, void *closure)
{
	puts("Cannot set CBFI stdout directly");
	Py_RETURN_NONE;
}

/* TODO:  expose stdout and memory via GetSetDef */

static PyObject *
CBFI_process_code(CBFI *self, PyObject *code, void *closure)
{
    PyObject *tmp;
    if (!PyUnicode_Check(code)) {
        PyErr_SetString(PyExc_TypeError, "The code must be a string");
        return NULL;
    }
    tmp = self->code;
    Py_INCREF(code);
    self->code = code;
    
    Py_ssize_t codelen = PyUnicode_GET_LENGTH(self->code);

    char current_symbol;
    while (self->codeptr<codelen){
    	self->steps_taken++;
    	//process symbol
      current_symbol = PyUnicode_ReadChar(self->code, self->codeptr);
    	switch (self->bounce_dir){
    	case NONE:
    		switch (current_symbol){
    		case '+': self->memory[self->memptr]++; break;
    		case '-': self->memory[self->memptr]--; break;
    		case '>': self->memptr++;
                      if(self->memptr>MEMSIZE){self->memptr = 0;}; break;
    		case '<': self->memptr--;
                      if(self->memptr<0){self->memptr = MEMSIZE;}; break;
    		case '.':
             self->_stdout[self->stdoutptr++] = self->memory[self->memptr]; break;
    		case ',': self->memory[self->memptr] = self->_stdin[self->stdinptr++]; break;
    		case ']': if(self->memory[self->memptr]) self->bounce_dir = LEFT; break;
    		case '[': if(!self->memory[self->memptr]) self->bounce_dir = RIGHT; break;
    		default: break;
    		} break;
    	case LEFT:
    		switch (current_symbol){
    		case ']': self->brkt_depth++; break;
    		case '[': self->brkt_depth==0?self->bounce_dir=NONE:self->brkt_depth--; break;
    		default: break;
    		} break;
    	case RIGHT:
    		switch (current_symbol){
    		case '[': self->brkt_depth++; break;
    		case ']': self->brkt_depth==0?self->bounce_dir=NONE:self->brkt_depth--; break;
    		default: break;
    		} break;
	}
	switch (self->bounce_dir){
	case NONE:  self->codeptr++; break;
	case LEFT:  self->codeptr--; break;
	case RIGHT: self->codeptr++; break;
	default: break;
	}
    }


    Py_DECREF(tmp);
    Py_RETURN_NONE;
}


/* CBFI data members*/
static PyMemberDef CBFI_members[] = {
    {"steps_taken", T_INT, offsetof(CBFI, steps_taken), 0,
     "Number of steps the interpreter has taken"},
    {NULL}  /* Sentinel */
};
static PyMethodDef CBFI_methods[] = {
    {"process_code", (PyCFunction) CBFI_process_code, METH_O,
     "Returns internal state and bumps it"},
    {"peekmem", (PyCFunction) CBFI_peekmem, METH_NOARGS,
     "Peeks into BFI memory"},
    {"dumpstdout", (PyCFunction) CBFI_dumpstdout, METH_NOARGS,
     "Dumps stdout to stdout"},
    {NULL}  /* Sentinel */
};

static PyGetSetDef CBFI_getsetters[] = {
    {"memory", (getter) CBFI_getmem, (setter) CBFI_setmem,
     "copy of interpreter's memory", NULL},
    {"stdout", (getter) CBFI_getstdout, (setter) CBFI_setstdout,
     "copy of interpreter's stdout", NULL},
    {NULL}  /* Sentinel */
};

static PyTypeObject CBFIType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "spam.CBFI",
    .tp_doc = "BF interpreter on some steroids",
    .tp_basicsize = sizeof(CBFI),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = CBFI_new,
    .tp_init = (initproc) CBFI_init,
    .tp_dealloc = (destructor) CBFI_dealloc,
    .tp_members = CBFI_members,
    .tp_methods = CBFI_methods,
    .tp_getset = CBFI_getsetters,
};

/* End BF impl*/

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",   /* name of module */
    "This is a spam documentation", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    SpamMethods
};


PyMODINIT_FUNC
PyInit_spam(void)
{
    PyObject *m;
    if (PyType_Ready(&CustomType) < 0)
        return NULL;

    if (PyType_Ready(&CBFIType) < 0)
        return NULL;

    m = PyModule_Create(&spammodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&CustomType);
    if (PyModule_AddObject(m, "FunProcessor", (PyObject *) &CustomType) < 0) {
        Py_DECREF(&CustomType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&CBFIType);
    if (PyModule_AddObject(m, "CBFI", (PyObject *) &CBFIType) < 0) {
        Py_DECREF(&CBFIType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
