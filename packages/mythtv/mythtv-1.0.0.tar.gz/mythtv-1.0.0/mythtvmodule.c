//
// Created by matthias on 08.05.22.
//

#define PY_SSIZE_T_CLEAN

#include <Python.h>

#include <fcntl.h>

// ---------------------------------------------------------------------------------------------------------------------

#define CHUNK_SIZE 8192

static PyObject *MythTVError;

PyObject *mythtv_filehash(PyObject *self, PyObject *args);

const char *filehash(char *buffer, size_t size, const char *filename);

// ---------------------------------------------------------------------------------------------------------------------

static PyMethodDef MythTVMethods[] = {
        {"filehash", mythtv_filehash, METH_VARARGS,
                "Execute a shell command."},
        {NULL, NULL, 0, NULL}        /* Sentinel */
};

// ---------------------------------------------------------------------------------------------------------------------

static struct PyModuleDef mythtvmodule = {
        PyModuleDef_HEAD_INIT,
        "mythtv",   /* name of module */
        "docs", /* module documentation, may be NULL */
        -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
        MythTVMethods
};

// ---------------------------------------------------------------------------------------------------------------------

PyMODINIT_FUNC PyInit_mythtv(void) {
    PyObject *m;

    m = PyModule_Create(&mythtvmodule);
    if (m == NULL)
        return NULL;

    MythTVError = PyErr_NewException("mythtv.error", NULL, NULL);
    Py_XINCREF(MythTVError);
    if (PyModule_AddObject(m, "error", MythTVError) < 0) {
        Py_XDECREF(MythTVError);
        Py_CLEAR(MythTVError);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}

// ---------------------------------------------------------------------------------------------------------------------

PyObject *mythtv_filehash(PyObject *self, PyObject *args) {

    char *filename = 0;

    if (PyArg_ParseTuple(args, "s", &filename) == 0) {
        return 0;
    }

    char hash[17];
    filehash(hash, sizeof(hash), filename);

    return Py_BuildValue("s", hash);

}

// ---------------------------------------------------------------------------------------------------------------------

const char *filehash(char *buffer, size_t size, const char *filename) {

    struct stat64 stat;
    uint64_t chunk[CHUNK_SIZE];

    int fd = open(filename, O_LARGEFILE | O_RDONLY);
    if (fd < 0) {
        fprintf(stderr, "can't open file %s, error: %s",
                filename, strerror(errno));
        return 0;
    }

    if (fstat64(fd, &stat) < 0) {
        fprintf(stderr, "can't stat file %s, error: %s",
                filename, strerror(errno));
        close(fd);
        return 0;
    }

    uint64_t hash = stat.st_size;

    if (lseek(fd, 0, SEEK_SET) < 0) {
        fprintf(stderr, "can't seek file %s, error: %s",
                filename, strerror(errno));
        close(fd);
        return 0;
    }

    if (read(fd, chunk, sizeof(chunk)) < 0) {
        fprintf(stderr, "can't read file %s, errno: %d, error: %s",
                filename, errno, strerror(errno));
        close(fd);
        return 0;
    }

    for (int i = 0; i < CHUNK_SIZE; i++) {
        hash += chunk[i];
    }

    if (lseek(fd, -sizeof(chunk), SEEK_END) < 0) {
        fprintf(stderr, "can't seek file %s, errno: %d, error: %s",
                filename, errno, strerror(errno));
        close(fd);
        return 0;
    }

    if (read(fd, chunk, sizeof(chunk)) < 0) {
        fprintf(stderr, "can't read file %s, errno: %d, error: %s",
                filename, errno, strerror(errno));
        close(fd);
        return 0;
    }

    for (int i = 0; i < CHUNK_SIZE; i++) {
        hash += chunk[i];
    }

    for (int i = 15; i >= 0; i--) {
        uint8_t nibble = hash & 0x0F;
        if (nibble < 10) {
            buffer[i] = '0' + nibble;
        } else {
            buffer[i] = 'a' + nibble - 10;
        }
        hash >>= 4;
    }
    buffer[16] = 0;

    close(fd);
    return buffer;

}

// ---------------------------------------------------------------------------------------------------------------------
