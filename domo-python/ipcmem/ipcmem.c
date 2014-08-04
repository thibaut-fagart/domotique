/*
 * ipcmemmodule.c (clh, 02/02/05)
 *
 * provides a IPC shared memory API
 *
 * - getid
 * - rmid
 * - attach
 * - detach
 *
 * provides also read and write for shared memory transfers
 */

#include "Python.h" 

#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>

static PyObject *IpcmemError; /* Exception ipcmem.error */

/* Set a  system specific error from errno, and return NULL */

static PyObject * ipcmem_error(void)
{
    return PyErr_SetFromErrno(IpcmemError);
}

/* Insert a constant value definition */

static int
ins( PyObject* d, char* symbol, long value )
{
        PyObject* v = PyInt_FromLong(value);
        if (!v || PyDict_SetItemString(d, symbol, v) < 0)
                return -1;                   /* triggers fatal error */

        Py_DECREF(v);
        return 0;
}

/* Module ipcmem */

static char ipcmem_ftok__doc__[] = "path, proj_id -> id\n\n\
Generate a system V IPC key for a path and proj_id";

static PyObject *ipcmem_ftok(PyObject *self, PyObject *args)
{
    int   pathsize, proj_id;
    char *path;
    key_t key;

    if (!PyArg_ParseTuple(args, "s#i",  &path, &pathsize, &proj_id )) {
        return NULL;
    }
    key = ftok( path, proj_id );
    if( key == -1 )
        return ipcmem_error();
    return PyInt_FromLong( (long)key);
}

static char ipcmem_getid__doc__[] = "key, size, perm -> id\n\n\
Get or create a shared memory segment";

static PyObject *ipcmem_getid(PyObject *self, PyObject *args)
{
    int key, size, perm;
    int shmid;

    if (!PyArg_ParseTuple(args, "iii", &key, &size, &perm)) {
        return NULL;
    }
    shmid = shmget( key, size, perm );
    if( shmid < 0)
        return ipcmem_error();
    return PyInt_FromLong( (long)shmid);
}

static char ipcmem_rmid__doc__[] = "id -> None\n\n\
Remove a shared memory";

static PyObject *ipcmem_rmid(PyObject *self, PyObject *args)
{
    int shmid;
    int err;

    if (!PyArg_ParseTuple(args, "i", &shmid))
        return NULL;
    err = shmctl( shmid, IPC_RMID, (struct shmid_ds *)0 );
    if( err < 0 )
	    return ipcmem_error();
    Py_INCREF(Py_None);
    return Py_None;
}

static char ipcmem_attach__doc__[] = "id, addr, flags -> pointer\n\n\
Attach shared memory segment";

static PyObject *ipcmem_attach(PyObject *self, PyObject *args)
{
    int   shmid, flags;
    long long addr;
    void *ptr;

    if (!PyArg_ParseTuple(args, "iLi", &shmid, &addr, &flags)) {
        return NULL;
    }
    ptr = shmat( shmid, (void *)addr, flags );
    if (!ptr)
	    return ipcmem_error();
    return PyInt_FromLong( (long)ptr);
}

static char ipcmem_detach__doc__[] = "address -> None\n\n\
Detach a shared memory";

static PyObject *ipcmem_detach(PyObject *self, PyObject *args)
{
    int err;
    long long addr;

    if (!PyArg_ParseTuple(args, "L", &addr))
        return NULL;
    err = shmdt( (void *)addr );
    if( err < 0 )
	    return ipcmem_error();
    Py_INCREF(Py_None);
    return Py_None;
}

static char ipcmem_read__doc__[] = "address, size -> data\n\n\
Read size bytes in shared memory at given address";

static PyObject *ipcmem_read(PyObject *self, PyObject *args)
{
    int size;
    long long addr;

    if (!PyArg_ParseTuple(args, "Li", &addr, &size)) {
        return NULL;
    }
    return PyString_FromStringAndSize((char *)addr, size);
}

static char ipcmem_write__doc__[] = "address, data -> None\n\n\
Write data in shared memory at given address";

static PyObject *ipcmem_write(PyObject *self, PyObject *args)
{
    int size;
    long long addr;
    char *buf;
    
    if (!PyArg_ParseTuple(args, "Ls#", &addr, &buf, &size)) {
        return NULL;
    }

    memcpy((char *)addr, buf, size);
    Py_INCREF(Py_None);
    return Py_None;
}

static char ipcmem__doc__[] = "\
This module provides a IPC shared memory API:\n\n\
- getid, rmid, attach, detach, read, write (shared memory) ";

static PyMethodDef ipcmem_methods[] = {
    {"ftok",  ipcmem_ftok,   METH_VARARGS, ipcmem_ftok__doc__},
    {"getid", ipcmem_getid,  METH_VARARGS, ipcmem_getid__doc__},
    {"rmid",  ipcmem_rmid,   METH_VARARGS, ipcmem_rmid__doc__},
    {"attach",ipcmem_attach, METH_VARARGS, ipcmem_attach__doc__},
    {"detach",ipcmem_detach, METH_VARARGS, ipcmem_detach__doc__},
    {"read",  ipcmem_read,   METH_VARARGS, ipcmem_read__doc__},
    {"write", ipcmem_write,  METH_VARARGS, ipcmem_write__doc__},
    {NULL,        NULL}        /* sentinel */
};

DL_EXPORT(void)
initipcmem()
{
    PyObject *m, *d;

    m = Py_InitModule4("ipcmem", ipcmem_methods, ipcmem__doc__,
		       (PyObject*)NULL, PYTHON_API_VERSION);
    d = PyModule_GetDict(m);
    ins(d, "IPC_CREAT",     IPC_CREAT);
    ins(d, "IPC_EXCL",      IPC_EXCL);
    ins(d, "IPC_PRIVATE",   IPC_PRIVATE);
    //ins(d, "PAGE_SIZE",     PAGE_SIZE);  where is it defined ?
    ins(d, "SHM_REMAP",       SHM_REMAP); 

    /* Initialize exception */
    IpcmemError = PyErr_NewException("ipcmem.error", NULL, NULL);
    if (IpcmemError != NULL)
        PyDict_SetItemString(d, "error", IpcmemError);
}
