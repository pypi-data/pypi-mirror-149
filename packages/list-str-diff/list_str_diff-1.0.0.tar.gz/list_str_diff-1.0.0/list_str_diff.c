#include <Python.h>

static PyObject *method_list_str_diff(PyObject *self, PyObject *args) {

    PyObject *letters;
    char *word;


    if(!PyArg_ParseTuple(args, "Os", &letters, &word)) {
        return NULL;
    }

    int len_letters = PyList_Size(letters);
    size_t len_word = strlen(word);

    char *word_copy = (char*)malloc(len_word * sizeof(char));
    strncpy(word_copy, word, len_word);

    PyObject *ret_list = PyList_New(0);

    int in_flag;

    for (int i = 0; i < len_letters; i++){

        PyObject *item = PyList_GetItem(letters, i);
        char *c_item = PyUnicode_AsUTF8(item);

        in_flag = 0;

        for (int j = 0; j < len_word; j++){
            if (*c_item == word[j]){
                word[j] = '\1';
                in_flag = 1;
                break;
            }
        }
        if (!in_flag){
            PyList_Append(ret_list, item);
        }
    }

    strncpy(word, word_copy, len_word);
    free(word_copy);

    return ret_list;
}


static PyMethodDef list_str_diffMethods[] = {
    {"list_str_diff", method_list_str_diff, METH_VARARGS, "Takes the difference of a list and a string."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef list_str_diff = {
    PyModuleDef_HEAD_INIT,
    "list_str_diff",
    "Takes the difference of a list and a string.",
    -1,
    list_str_diffMethods
};


PyMODINIT_FUNC PyInit_list_str_diff(void) {
    return PyModule_Create(&list_str_diff);
}
