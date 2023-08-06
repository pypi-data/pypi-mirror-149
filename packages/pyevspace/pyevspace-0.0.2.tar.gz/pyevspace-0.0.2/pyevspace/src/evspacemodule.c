#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

typedef struct {
	PyObject_HEAD
	double m_arr[3];
} EVector;

static PyTypeObject EVectorType;

typedef struct {
	PyObject_HEAD
	double m_arr[3][3];
} EMatrix;

static PyTypeObject EMatrixType;

#define EVSPACE_MODULE
#include <evspacemodule.h>

#define EVSpace_RADIANS_TO_DEGREES 180.0 / 3.14159265358979323846

/*************************************/
/*	implimentation of C API methods  */
/*************************************/

// MAJOR TODO: change naming convention to EVSpace_Mat_XXX or EVSpace_Vec_XXX for ALL methods not just numeric methods

/************** EVector **************/

static EVector* EVSpace_Vector_add(const EVector* lhs, const EVector* rhs)
{
	EVector* rtn = (EVector*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	rtn->m_arr[0] = lhs->m_arr[0] + rhs->m_arr[0];
	rtn->m_arr[1] = lhs->m_arr[1] + rhs->m_arr[1];
	rtn->m_arr[2] = lhs->m_arr[2] + rhs->m_arr[2];

	return rtn;
}

static EVector* EVSpace_Vector_sub(const EVector* lhs, const EVector* rhs)
{
	EVector* rtn = (EVector*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	rtn->m_arr[0] = lhs->m_arr[0] - rhs->m_arr[0];
	rtn->m_arr[1] = lhs->m_arr[1] - rhs->m_arr[1];
	rtn->m_arr[2] = lhs->m_arr[2] - rhs->m_arr[2];

	return rtn;
}

static EVector* EVSpace_Vector_mult(const EVector* lhs, double rhs)
{
	EVector* rtn = (EVector*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	rtn->m_arr[0] = lhs->m_arr[0] * rhs;
	rtn->m_arr[1] = lhs->m_arr[1] * rhs;
	rtn->m_arr[2] = lhs->m_arr[2] * rhs;

	return rtn;
}

static EVector* EVSpace_Vector_neg(const EVector* lhs)
{
	EVector* rtn = (EVector*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	rtn->m_arr[0] = -lhs->m_arr[0];
	rtn->m_arr[1] = -lhs->m_arr[1];
	rtn->m_arr[2] = -lhs->m_arr[2];

	return rtn;
}

static double EVSpace_Vector_abs(const EVector* vec)
{
	return sqrt(vec->m_arr[0] * vec->m_arr[0]
		+ vec->m_arr[1] * vec->m_arr[1]
		+ vec->m_arr[2] * vec->m_arr[2]);
}

static void EVSpace_Vector_iadd(EVector* lhs, const EVector* rhs)
{
	lhs->m_arr[0] += rhs->m_arr[0];
	lhs->m_arr[1] += rhs->m_arr[1];
	lhs->m_arr[2] += rhs->m_arr[2];
}

static void EVSpace_Vector_isub(EVector* lhs, const EVector* rhs)
{
	lhs->m_arr[0] -= rhs->m_arr[0];
	lhs->m_arr[1] -= rhs->m_arr[1];
	lhs->m_arr[2] -= rhs->m_arr[2];
}

static void EVSpace_Vector_imult(EVector* lhs, double rhs)
{
	lhs->m_arr[0] *= rhs;
	lhs->m_arr[1] *= rhs;
	lhs->m_arr[2] *= rhs;
}

static EVector* EVSpace_Vector_div(const EVector* lhs, double rhs)
{
	EVector* rtn = (EVector*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	rtn->m_arr[0] = lhs->m_arr[0] / rhs;
	rtn->m_arr[1] = lhs->m_arr[1] / rhs;
	rtn->m_arr[2] = lhs->m_arr[2] / rhs;

	return rtn;
}

static void EVSpace_Vector_idiv(EVector* lhs, double rhs)
{
	lhs->m_arr[0] /= rhs;
	lhs->m_arr[1] /= rhs;
	lhs->m_arr[2] /= rhs;
}

static int EVSpace_Vector_eq(const EVector* lhs, const EVector* rhs)
{
	static double epsilon = 1e-6;
	if ((fabs(lhs->m_arr[0] - rhs->m_arr[0]) < epsilon) 
		&& (fabs(lhs->m_arr[1] - rhs->m_arr[1]) < epsilon) 
		&& (fabs(lhs->m_arr[2] - rhs->m_arr[2]) < epsilon))
		return 1;
	return 0;
}

static int EVSpace_Vector_ne(const EVector* lhs, const EVector* rhs)
{
	if (EVSpace_Vector_eq(lhs, rhs))
		return 0;
	return 1;
}

static double EVSpace_Vector_dot(const EVector* lhs, const EVector* rhs)
{
	return (lhs->m_arr[0] * rhs->m_arr[0])
		+ (lhs->m_arr[1] * rhs->m_arr[1])
		+ (lhs->m_arr[2] * rhs->m_arr[2]);
}

static EVector* EVSpace_Vector_cross(const EVector* lhs, const EVector* rhs)
{
	EVector* rtn = (EVector*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	rtn->m_arr[0] = ((lhs->m_arr[1] * rhs->m_arr[2]) - (lhs->m_arr[2] * rhs->m_arr[1]));
	rtn->m_arr[1] = ((lhs->m_arr[2] * rhs->m_arr[0]) - (lhs->m_arr[0] * rhs->m_arr[2]));
	rtn->m_arr[2] = ((lhs->m_arr[0] * rhs->m_arr[1]) - (lhs->m_arr[1] * rhs->m_arr[0]));

	return rtn;
}

static double EVSpace_vector_mag(const EVector* vec)
{
	return sqrt(EVSpace_Vector_dot(vec, vec));
}

static double EVSpace_Vector_mag2(const EVector* vec)
{
	return EVSpace_Vector_dot(vec, vec);
}

static EVector* EVSpace_Vector_norm(const EVector* vec)
{
	return EVSpace_Vector_div(vec, sqrt(EVSpace_Vector_dot(vec, vec)));
}

static void EVSpace_Vector_inorm(EVector* rtn)
{
	EVSpace_Vector_idiv(rtn, sqrt(EVSpace_Vector_dot(rtn, rtn)));
}

static double EVSpace_Vector_vang(const EVector* lhs, const EVector* rhs)
{
	double theta = acos(EVSpace_Vector_dot(lhs, rhs) / (EVSpace_vector_mag(lhs) * EVSpace_vector_mag(rhs)));
	return theta * EVSpace_RADIANS_TO_DEGREES;
}

static EVector* EVSpace_Vector_vxcl(const EVector* vec, const EVector* xcl)
{
	EVector* rtn = (EVector*)vec->ob_base.ob_type->tp_new(vec->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	double scale = EVSpace_Vector_dot(vec, xcl) / EVSpace_Vector_mag2(xcl);
	rtn->m_arr[0] = vec->m_arr[0] - (xcl->m_arr[0] * scale);
	rtn->m_arr[1] = vec->m_arr[1] - (xcl->m_arr[1] * scale);
	rtn->m_arr[2] = vec->m_arr[2] - (xcl->m_arr[2] * scale);

	return rtn;
}

/*********************************************/
/***************** EMatrix *******************/
/*********************************************/

static EMatrix* EVSpace_Matrix_add(const EMatrix* lhs, const EMatrix* rhs)
{
	EMatrix* rtn = (EMatrix*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			rtn->m_arr[i][j] = lhs->m_arr[i][j] + rhs->m_arr[i][j];
	}

	return rtn;
}

static EMatrix* EVSpace_Matrix_sub(const EMatrix* lhs, const EMatrix* rhs)
{
	EMatrix* rtn = (EMatrix*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			rtn->m_arr[i][j] = lhs->m_arr[i][j] - rhs->m_arr[i][j];
	}

	return rtn;
}

static EMatrix* EVSpace_Matrix_multm(const EMatrix* lhs, const EMatrix* rhs)
{
	EMatrix* rtn = (EMatrix*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			double sum = 0;
			for (int k = 0; k < 3; k++)
				sum += lhs->m_arr[i][k] * rhs->m_arr[k][j];
			rtn->m_arr[i][j] = sum;
		}
	}

	return rtn;
}

static EVector* EVSpace_Matrix_multv(const EMatrix* lhs, const EVector* rhs)
{
	EVector* rtn = (EVector*)rhs->ob_base.ob_type->tp_new(rhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		double sum = 0;
		for (int j = 0; j < 3; j++)
			sum += lhs->m_arr[i][j] * rhs->m_arr[j];
		rtn->m_arr[i] = sum;
	}

	return rtn;
}

static EMatrix* EVSpace_Matrix_multd(const EMatrix* lhs, double rhs)
{
	EMatrix* rtn = (EMatrix*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			rtn->m_arr[i][j] = lhs->m_arr[i][j] * rhs;
	}

	return rtn;
}

static EMatrix* EVSpace_Matrix_neg(const EMatrix* mat)
{
	EMatrix* rtn = (EMatrix*)mat->ob_base.ob_type->tp_new(mat->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			rtn->m_arr[i][j] = -mat->m_arr[i][j];
	}

	return rtn;
}

static void EVSpace_Matrix_iadd(EMatrix* lhs, const EMatrix* rhs)
{
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			lhs->m_arr[i][j] += rhs->m_arr[i][j];
	}
}

static void EVSpace_Matrix_isub(EMatrix* lhs, const EMatrix* rhs)
{
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			lhs->m_arr[i][j] -= rhs->m_arr[i][j];
	}
}

static void EVSpace_Matrix_imultm(EMatrix* lhs, const EMatrix* rhs)
{
	EMatrix* tmp = EVSpace_Matrix_multm(lhs, rhs);
	if (!tmp) {
		lhs = NULL;
		return;
	}

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			lhs->m_arr[i][j] = tmp->m_arr[i][j];
	}

	tmp->ob_base.ob_type->tp_dealloc((PyObject*)tmp);
}

static void EVSpace_Matrix_imultd(EMatrix* lhs, double rhs)
{
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			lhs->m_arr[i][j] *= rhs;
	}
}

static EMatrix* EVSpace_Matrix_div(const EMatrix* lhs, double rhs)
{
	EMatrix* rtn = (EMatrix*)lhs->ob_base.ob_type->tp_new(lhs->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			rtn->m_arr[i][j] = lhs->m_arr[i][j] / rhs;
	}

	return rtn;
}

static void EVSpace_Matrix_idiv(EMatrix* lhs, double rhs)
{
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			lhs->m_arr[i][j] /= rhs;
	}
}

static int EVSpace_Matrix_eq(const EMatrix* lhs, const EMatrix* rhs)
{
	static double epsilon = 1e-6;
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			if (fabs(lhs->m_arr[i][j] - rhs->m_arr[i][j]) > epsilon) 
				return 0;
		}
	}
	return 1;
}

static int EVSpace_Matrix_ne(const EMatrix* lhs, const EMatrix* rhs)
{
	if (EVSpace_Matrix_eq(lhs, rhs) == 1)
		return 0;
	return 1;
}

static double EVSpace_Matrix_det(const EMatrix* lhs)
{
	return lhs->m_arr[0][0] * ((lhs->m_arr[1][1] * lhs->m_arr[2][2]) - (lhs->m_arr[1][2] * lhs->m_arr[2][1]))
		+ lhs->m_arr[0][1] * ((lhs->m_arr[1][2] * lhs->m_arr[2][0]) - (lhs->m_arr[1][0] * lhs->m_arr[2][2]))
		+ lhs->m_arr[0][2] * ((lhs->m_arr[1][0] * lhs->m_arr[2][1]) - (lhs->m_arr[1][1] * lhs->m_arr[2][0]));
}

static EMatrix* EVSpace_Matrix_trans(const EMatrix* mat)
{
	EMatrix* rtn = (EMatrix*)mat->ob_base.ob_type->tp_new(mat->ob_base.ob_type, NULL, NULL);
	if (!rtn)
		return NULL;

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			rtn->m_arr[i][j] = mat->m_arr[j][i];
	}

	return rtn;
}

/****************************************************/
/*	Implimenting C API into Python number metehods  */
/****************************************************/

/****************************************************/
/************** EVector implementations *************/
/****************************************************/

/****************************************************/
/************* EVector Numeric Methods **************/
/****************************************************/

static PyObject* EVector_add(EVector* self, PyObject* arg)
{
	if (!PyObject_TypeCheck(arg, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	return (PyObject*)EVSpace_Vector_add(self, (EVector*)arg);
}

static PyObject* EVector_sub(EVector* self, PyObject* arg)
{
	if (!PyObject_TypeCheck(arg, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	return (PyObject*)EVSpace_Vector_sub(self, (EVector*)arg);
}

static PyObject* EVector_mult(EVector* self, PyObject* arg)
{
	double rhs;
	
	if (PyFloat_CheckExact(arg))
		rhs = PyFloat_AS_DOUBLE(arg);
	else if (PyLong_CheckExact(arg)) {
		rhs = PyLong_AsDouble(arg);
		if (PyErr_Occurred())
			return NULL;
	}
	else
		Py_RETURN_NOTIMPLEMENTED;

	return (PyObject*)EVSpace_Vector_mult(self, rhs);
}

static PyObject* EVector_neg(EVector* self)
{
	return (PyObject*)EVSpace_Vector_neg(self);
}

static PyObject* EVector_abs(EVector* self)
{
	return (PyObject*)PyFloat_FromDouble(EVSpace_Vector_abs(self));
}

static PyObject* EVector_iadd(EVector* self, PyObject* arg)
{
	if (!PyObject_TypeCheck(arg, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	EVSpace_Vector_iadd(self, (EVector*)arg);
	return Py_NewRef(self);
}

static PyObject* EVector_isub(EVector* self, PyObject* arg)
{
	if (!PyObject_TypeCheck(arg, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	EVSpace_Vector_isub(self, (EVector*)arg);
	return Py_NewRef(self);
}

static PyObject* EVector_imult(EVector* self, PyObject* arg)
{
	double rhs;
	if (PyFloat_CheckExact(arg))
		rhs = PyFloat_AS_DOUBLE(arg);
	else if (PyLong_CheckExact(arg)) {
		rhs = PyLong_AsDouble(arg);
		if (PyErr_Occurred())
			return NULL;
	}
	else
		Py_RETURN_NOTIMPLEMENTED;

	EVSpace_Vector_imult(self, rhs);
	return Py_NewRef(self);
}

static PyObject* EVector_div(EVector* self, PyObject* arg)
{
	double rhs;
	if (PyFloat_CheckExact(arg))
		rhs = PyFloat_AS_DOUBLE(arg);
	else if (PyLong_CheckExact(arg)) {
		rhs = PyLong_AsDouble(arg);
		if (PyErr_Occurred())
			return NULL;
	}
	else
		Py_RETURN_NOTIMPLEMENTED;

	return (PyObject*)EVSpace_Vector_div(self, rhs);
}

static PyObject* EVector_idiv(EVector* self, PyObject* arg)
{
	double rhs;
	if (PyFloat_CheckExact(arg))
		rhs = PyFloat_AS_DOUBLE(arg);
	else if (PyLong_CheckExact(arg)) {
		rhs = PyLong_AsDouble(arg);
		if (PyErr_Occurred())
			return NULL;
	}
	else
		Py_RETURN_NOTIMPLEMENTED;

	EVSpace_Vector_idiv(self, rhs);
	return Py_NewRef(self);
}

static PyNumberMethods EVector_NBMethods = {
	.nb_add = (binaryfunc)EVector_add,
	.nb_subtract = (binaryfunc)EVector_sub,
	.nb_multiply = (binaryfunc)EVector_mult,
	.nb_negative = (unaryfunc)EVector_neg,
	.nb_absolute = (unaryfunc)EVector_abs,
	.nb_inplace_add = (binaryfunc)EVector_iadd,
	.nb_inplace_subtract = (binaryfunc)EVector_isub,
	.nb_inplace_multiply = (binaryfunc)EVector_imult,
	.nb_true_divide = (binaryfunc)EVector_div,
	.nb_inplace_true_divide = (binaryfunc)EVector_idiv,
};

/****************************************************/
/************** EVector Class Methods ***************/
/****************************************************/

static PyObject* EVector_Mag(EVector* self, PyObject* UNUSED)
{
	return PyFloat_FromDouble(EVSpace_vector_mag(self));
}

static PyObject* EVector_Mag2(EVector* self, PyObject* UNUSED)
{
	return PyFloat_FromDouble(EVSpace_Vector_mag2(self));
}

static PyObject* EVector_Normalize(EVector* self, PyObject* UNUSED)
{
	EVSpace_Vector_inorm(self);
	Py_RETURN_NONE;
}

static PyMethodDef EVector_Methods[] = {
	{"mag", (PyCFunction)EVector_Mag, METH_NOARGS, "Returns the magnitude of an EVector."},
	{"mag2", (PyCFunction)EVector_Mag2, METH_NOARGS, "Returns the square of the magnitude of an EVector."},
	{"normalize", (PyCFunction)EVector_Normalize, METH_NOARGS, "Normalized an EVector."},
	{NULL}
};

/****************************************************/
/************* EVector Module Methods ***************/
/****************************************************/

static PyObject* EVector_Dot(PyObject* UNUSED, PyObject *const *args, Py_ssize_t size)
{
	if (size != 2) {
		PyErr_SetString(PyExc_TypeError, "dot() takes exactly 2 arguments");
		return NULL;
	}
 
	EVector* lhs = (EVector*)args[0];
	EVector* rhs = (EVector*)args[1];

	if (!lhs && !rhs) {
		PyErr_SetString(PyExc_ValueError, "Arguments cannot be NULL.");
		return NULL;
	}
	if (!PyObject_TypeCheck(lhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "First argument must be EVector type.");
		return NULL;
	}
	if (!PyObject_TypeCheck(rhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "Second argument must be EVector type.");
		return NULL;
	}

	return PyFloat_FromDouble(EVSpace_Vector_dot(lhs, rhs));
}

static PyObject* EVector_Cross(PyObject* UNUSED, PyObject* const* args, Py_ssize_t size)
{
	if (size != 2) {
		PyErr_SetString(PyExc_TypeError, "cross() takes exactly two arguments");
		return NULL;
	}

	EVector* lhs = (EVector*)args[0];
	EVector* rhs = (EVector*)args[1];

	if (!lhs && !rhs) {
		PyErr_SetString(PyExc_ValueError, "Arguments cannot be NULL.");
		return NULL;
	}
	if (!PyObject_TypeCheck(lhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "First argument must be EVector type.");
		return NULL;
	}
	if (!PyObject_TypeCheck(rhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "Second argument must be EVector type.");
		return NULL;
	}

	EVector* rtn = EVSpace_Vector_cross(lhs, rhs);

	return (PyObject*)(rtn);
}

static PyObject* EVector_Norm(PyObject* UNUSED, PyObject* const* args, Py_ssize_t size)
{
	if (size != 1) {
		PyErr_SetString(PyExc_TypeError, "norm() takes exactly one argument");
		return NULL;
	}

	EVector* lhs = (EVector*)args[0];

	if (!lhs) {
		PyErr_SetString(PyExc_ValueError, "Arguments cannot be NULL.");
		return NULL;
	}
	if (!PyObject_TypeCheck(lhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "First argument must be EVector type.");
		return NULL;
	}

	return (PyObject*)EVSpace_Vector_norm(lhs);
}

static PyObject* EVector_Vang(PyObject* UNUSED, PyObject* const* args, Py_ssize_t size)
{
	if (size != 2) {
		PyErr_SetString(PyExc_TypeError, "vang takes exactly two arguments");
		return NULL;
	}

	EVector* lhs = (EVector*)args[0];
	EVector* rhs = (EVector*)args[1];

	if (!lhs && !rhs) {
		PyErr_SetString(PyExc_ValueError, "Arguments cannot be NULL.");
		return NULL;
	}
	if (!PyObject_TypeCheck(lhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "First argument must be EVector type.");
		return NULL;
	}
	if (!PyObject_TypeCheck(rhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "Second argument must be EVector type.");
		return NULL;
	}

	return PyFloat_FromDouble(EVSpace_Vector_vang(lhs, rhs));
}

static PyObject* EVector_Vxcl(PyObject* UNUSED, PyObject* const* args, Py_ssize_t size)
{
	if (size != 2) {
		PyErr_SetString(PyExc_TypeError, "vxcl() takes exactly two arguments");
		return NULL;
	}

	EVector* lhs = (EVector*)args[0];
	EVector* rhs = (EVector*)args[1];

	if (!lhs && !rhs) {
		PyErr_SetString(PyExc_ValueError, "Arguments cannot be NULL.");
		return NULL;
	}
	if (!PyObject_TypeCheck(lhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "First argument must be EVector type.");
		return NULL;
	}
	if (!PyObject_TypeCheck(rhs, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "Second argument must be EVector type.");
		return NULL;
	}

	return (PyObject*)(EVSpace_Vector_vxcl(lhs, rhs));
}

static PyMethodDef EVector_ModuleMethods[] = {
	{"dot", (PyCFunction)EVector_Dot, METH_FASTCALL, "Returns the dot product or inner produce of two EVectors."},
	{"cross", (PyCFunction)EVector_Cross, METH_FASTCALL, "Returns the cross product of two EVectors."},
	{"norm", (PyCFunction)EVector_Norm, METH_FASTCALL, "Returns a normalized version of an EVector."},
	{"vang", (PyCFunction)EVector_Vang, METH_FASTCALL, "Returns the shortest angle between two EVector's."},
	{"vxcl", (PyCFunction)EVector_Vxcl, METH_FASTCALL, "Returns a vector exculded from another."},
	{NULL}
};

/****************************************************/
/************* EVector Sequence Methods *************/
/****************************************************/

static Py_ssize_t EVector_length(EVector* self)
{
	return 3;
}

static PyObject* EVector_get(EVector* self, Py_ssize_t index)
{
	if (index < 0 || index > 2) {
		PyErr_SetString(PyExc_ValueError, "Index out of bounds.");
		return NULL;
	}

	return PyFloat_FromDouble(self->m_arr[index]);
}

static int EVector_set(EVector* self, Py_ssize_t index, PyObject* val)
{
	if (index < 0 || index > 2) {
		PyErr_SetString(PyExc_ValueError, "Index out of bounds.");
		return -1;
	}

	if (PyFloat_CheckExact(val))
		self->m_arr[index] = PyFloat_AS_DOUBLE(val);
	else if (PyLong_CheckExact(val)) {
		double rhs = PyLong_AsDouble(val);
		if (PyErr_Occurred())
			return -1;
		self->m_arr[index] = rhs;
	}
	else {
		PyErr_SetString(PyExc_TypeError, "Assignment value must be float or int type.");
	}

	return 0;
}

static PySequenceMethods EVector_sequence = {
	.sq_length = (lenfunc)EVector_length,
	.sq_item = (ssizeargfunc)EVector_get,
	.sq_ass_item = (ssizeobjargproc)EVector_set,
};

/****************************************************/
/************** EVector Type Methods ****************/
/****************************************************/

static int EVector_init(EVector* self, PyObject* args, PyObject* kwds)
{
	double x = 0, y = 0, z = 0;
	static char* kwlist[] = { "x", "y", "z", NULL };
		
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ddd", kwlist, &x, &y, &z))
		return -1;

	self->m_arr[0] = x;
	self->m_arr[1] = y;
	self->m_arr[2] = z;

	return 0;
}

static PyObject* EVector_str(const EVector* vec)
{
	char buffer[50]; // todo: find the accurate number here
	int ok = snprintf(buffer, 50, "[ %f, %f, %f ]", vec->m_arr[0], vec->m_arr[1], vec->m_arr[2]);

	if (ok < 0 || ok > 50) {
		PyErr_SetString(PyExc_BufferError, "Buffer too small to create string.");
		return NULL;
	}
	
	return Py_BuildValue("s#", buffer, strlen(buffer));
}

static PyObject* EVector_richcompare(PyObject* self, PyObject* other, int op)
{
	if (!PyObject_TypeCheck(other, self->ob_type)) {
		PyErr_SetString(PyExc_TypeError, "Argument must be EVector type.");
		return NULL;
	}

	switch (op) {
	case Py_EQ:
		return PyBool_FromLong(EVSpace_Vector_eq((EVector*)self, (EVector*)other));
	case Py_NE:
		return PyBool_FromLong(EVSpace_Vector_ne((EVector*)self, (EVector*)other));
	default:
		Py_RETURN_NOTIMPLEMENTED;
	}
}

PyDoc_STRVAR(evector_doc, "Euclidean vector object to represent a spatial vector in three dimensional space.");

static PyTypeObject EVectorType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	.tp_name		= "pyevspace.EVector",
	.tp_doc			= evector_doc,
	.tp_basicsize	= sizeof(EVector),
	.tp_itemsize	= 0,
	.tp_flags		= Py_TPFLAGS_DEFAULT, // todo: do we want to set Py_TPFLAGS_SEQUENCE flag?
	.tp_new			= PyType_GenericNew,
	.tp_init		= (initproc)EVector_init,
	.tp_methods		= EVector_Methods,
	.tp_str			= (reprfunc)EVector_str,
	.tp_as_number	= &EVector_NBMethods,
	.tp_richcompare	= (richcmpfunc)EVector_richcompare,
	.tp_as_sequence = &EVector_sequence,
};

/****************************************************/
/************** EMatrix implementation **************/
/****************************************************/

/****************************************************/
/************* EMatrix Numeric Methods **************/
/****************************************************/

static PyObject* EMatrix_add(EMatrix* self, PyObject* args)
{
	if (!PyObject_TypeCheck(args, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	return (PyObject*)EVSpace_Matrix_add(self, (EMatrix*)args);
}

static PyObject* EMatrix_sub(EMatrix* self, PyObject* args)
{
	if (!PyObject_TypeCheck(args, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	return (PyObject*)EVSpace_Matrix_sub(self, (EMatrix*)args);
}

static PyObject* EMatrix_mult(EMatrix* self, PyObject* args)
{
	if (PyFloat_CheckExact(args))
		return (PyObject*)EVSpace_Matrix_multd(self, PyFloat_AS_DOUBLE(args));
	else if (PyLong_CheckExact(args)) {
		double rhs = PyLong_AsDouble(args);
		if (PyErr_Occurred())
			return NULL;

		return (PyObject*)EVSpace_Matrix_multd(self, PyLong_AsDouble(args));
	}
	else
		Py_RETURN_NOTIMPLEMENTED;
}

static PyObject* EMatrix_mmult(EMatrix* self, PyObject* args)
{
	if (PyObject_TypeCheck(args, &EMatrixType))
		return (PyObject*)EVSpace_Matrix_multm(self, (EMatrix*)args);
	else if (PyObject_TypeCheck(args, &EVectorType))
		return (PyObject*)EVSpace_Matrix_multv(self, (EVector*)args);
	else
		Py_RETURN_NOTIMPLEMENTED;
}

static PyObject* EMatrix_neg(EMatrix* self, PyObject* UNUSED)
{
	return (PyObject*)EVSpace_Matrix_neg(self);
}

static PyObject* EMatrix_iadd(EMatrix* self, PyObject* args)
{
	if (!PyObject_TypeCheck(args, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	EVSpace_Matrix_iadd(self, (EMatrix*)args);
	return Py_NewRef(self);
}

static PyObject* EMatrix_isub(EMatrix* self, PyObject* args)
{
	if (!PyObject_TypeCheck(args, self->ob_base.ob_type))
		Py_RETURN_NOTIMPLEMENTED;

	EVSpace_Matrix_isub(self, (EMatrix*)args);
	return Py_NewRef(self);
}

static PyObject* EMatrix_imult(EMatrix* self, PyObject* args)
{
	if (PyFloat_CheckExact(args)) {
		EVSpace_Matrix_imultd(self, PyFloat_AS_DOUBLE(args));
		return Py_NewRef(self);
	}
	else if (PyLong_CheckExact(args)) {
		double rhs = PyLong_AsDouble(args);
		if (PyErr_Occurred())
			return NULL;

		EVSpace_Matrix_imultd(self, rhs);
		return Py_NewRef(self);
	}
	else
		Py_RETURN_NOTIMPLEMENTED;
}

static PyObject* EMatrix_mimult(EMatrix* self, PyObject* args)
{
	if (PyObject_TypeCheck(args, &EMatrixType)) {
		EVSpace_Matrix_imultm(self, (EMatrix*)args);
		return Py_NewRef(self);
	}
	else
		Py_RETURN_NOTIMPLEMENTED;
}

static PyObject* EMatrix_div(EMatrix* self, PyObject* args)
{
	double rhs;
	if (PyFloat_CheckExact(args))
		rhs = PyFloat_AS_DOUBLE(args);
	else if (PyLong_CheckExact(args)) {
		rhs = PyLong_AsDouble(args);
		if (PyErr_Occurred())
			return NULL;
	}
	else
		Py_RETURN_NOTIMPLEMENTED;

	return (PyObject*)EVSpace_Matrix_div(self, rhs);
}

static PyObject* EMatrix_idiv(EMatrix* self, PyObject* args)
{
	double rhs;
	if (PyFloat_CheckExact(args))
		rhs = PyFloat_AS_DOUBLE(args);
	else if (PyLong_CheckExact(args)) {
		rhs = PyLong_AsDouble(args);
		if (PyErr_Occurred())
			return NULL;
	}
	else
		Py_RETURN_NOTIMPLEMENTED;

	EVSpace_Matrix_idiv(self, rhs);
	return Py_NewRef(self);
}

// todo: split the multiply into multiply(float/int) and matrix multiply(vector/matrix)
static PyNumberMethods EMatrix_NBMethods = {
	.nb_add = (binaryfunc)EMatrix_add,
	.nb_subtract = (binaryfunc)EMatrix_sub,
	.nb_multiply = (binaryfunc)EMatrix_mult,
	.nb_negative = (unaryfunc)EMatrix_neg,
	.nb_inplace_add = (binaryfunc)EMatrix_iadd,
	.nb_inplace_subtract = (binaryfunc)EMatrix_isub,
	.nb_inplace_multiply = (binaryfunc)EMatrix_imult,
	.nb_true_divide = (binaryfunc)EMatrix_div,
	.nb_inplace_true_divide = (binaryfunc)EMatrix_idiv,
	.nb_matrix_multiply = (binaryfunc)EMatrix_mmult,
	.nb_inplace_matrix_multiply = (binaryfunc)EMatrix_mimult,
};

/****************************************************/
/************** EMatrix Class Methods ***************/
/****************************************************/

static PyObject* EMatrix_set(EMatrix* self, PyObject* args)
{
	int i, j;
	double val;

	if (!PyArg_ParseTuple(args, "lld", &i, &j, &val))
		return NULL;

	if (i < 0 || i > 2) {
		PyErr_SetString(PyExc_ValueError, "Row index out of bounds.");
		return NULL;
	}
	if (j < 0 || j > 2) {
		PyErr_SetString(PyExc_ValueError, "Column index out of bounds.");
		return NULL;
	}

	self->m_arr[i][j] = val;
	Py_RETURN_NONE;
}

static PyObject* EMatrix_get(EMatrix* self, PyObject* args)
{
	int i, j;

	if (!PyArg_ParseTuple(args, "ll", &i, &j))
		return NULL;

	if (i < 0 || i > 2) {
		PyErr_SetString(PyExc_ValueError, "Row index out of bounds.");
		return NULL;
	}
	if (j < 0 || j > 2) {
		PyErr_SetString(PyExc_ValueError, "Column index out of bounds.");
		return NULL;
	}

	return PyFloat_FromDouble(self->m_arr[i][j]);
}

// todo: can we manage these with a sequence like protocol?
static PyMethodDef EMatrix_Methods[] = {
	{"set", (PyCFunction)EMatrix_set, METH_VARARGS, "Sets a matrix comonent to a given value."},
	{"get", (PyCFunction)EMatrix_get, METH_VARARGS, "Returns a matrix comonent."},
	{NULL}
};

/****************************************************/
/************* EMatrix Module Methods ***************/
/****************************************************/

static PyObject* EMatrix_det(PyObject* UNUSED, PyObject* const* args, Py_ssize_t size)
{
	if (size != 1) {
		PyErr_SetString(PyExc_TypeError, "det takes exactly one argument");
		return NULL;
	}

	EMatrix* mat = (EMatrix*)args[0];

	if (!PyObject_TypeCheck(mat, &EMatrixType)) {
		PyErr_SetString(PyExc_TypeError, "Argument should be EMatrix type.");
		return NULL;
	}

	return PyFloat_FromDouble(EVSpace_Matrix_det(mat));
}

static PyObject* EMatrix_trans(PyObject* UNUSED, PyObject* const* args, Py_ssize_t size)
{
	if (size != 1) {
		PyErr_SetString(PyExc_TypeError, "transpose() takes exactly one argument");
		return NULL;
	}

	EMatrix* mat = (EMatrix*)args[0];

	if (!PyObject_TypeCheck(mat, &EMatrixType)) {
		PyErr_SetString(PyExc_TypeError, "Argument should be EMatrix type.");
		return NULL;
	}

	return (PyObject*)EVSpace_Matrix_trans(mat);
}

static PyMethodDef EMatrix_ModuleMethods[] = {
	{"det", (PyCFunction)EMatrix_det, METH_FASTCALL, "Returns the determinate of a matrix."},
	{"transpose", (PyCFunction)EMatrix_trans, METH_FASTCALL, "Returns the transpose of a matrix."},
	{NULL}
};

/****************************************************/
/************** EMatrix Type Methods ****************/
/****************************************************/

static int EMatrix_init(EMatrix* self, PyObject* args, PyObject* UNUSED)
{
	EVector* c0 = NULL, *c1 = NULL, *c2 = NULL;

	if (!PyArg_ParseTuple(args, "|OOO", &c0, &c1, &c2)) // todo: allow this to be a list or evector
		return -1;

	if (c0 && !PyObject_TypeCheck(c0, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "First argument must be EVector type.");
		return -1;
	}
	else if (c1 && !PyObject_TypeCheck(c1, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "Second argument must be EVector type.");
		return -1;
	}
	else if (c2 && !PyObject_TypeCheck(c2, &EVectorType)) {
		PyErr_SetString(PyExc_TypeError, "Third argument must be EVector type.");
		return -1;
	}

	// todo: can we do this more efficiently? we must be able to, too many loops here
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++)
			self->m_arr[i][j] = 0;
	}

	if (c0 != NULL) {
		for (int i = 0; i < 3; i++)
			self->m_arr[i][0] = c0->m_arr[i];
	}
	if (c1 != NULL) {
		for (int i = 0; i < 3; i++)
			self->m_arr[i][1] = c1->m_arr[i];
	}
	if (c2 != NULL) {
		for (int i = 0; i < 3; i++)
			self->m_arr[i][2] = c2->m_arr[i];
	}

	return 0;
}

static PyObject* EMatrix_str(const EMatrix* mat)
{
	const static int sz_buffer = 200;
	char buffer[200]; // todo: find the accurate number here
	int ok = snprintf(buffer, sz_buffer, "[ %f, %f, %f ]\n[ %f, %f, %f ]\n[ %f, %f, %f ]",
		mat->m_arr[0][0], mat->m_arr[0][1], mat->m_arr[0][2],
		mat->m_arr[1][0], mat->m_arr[1][1], mat->m_arr[1][2],
		mat->m_arr[2][0], mat->m_arr[2][1], mat->m_arr[2][2]);

	if (ok < 0 || ok > sz_buffer) {
		PyErr_SetString(PyExc_BufferError, "Buffer too small to create string.");
		return NULL;
	}

	return Py_BuildValue("s#", buffer, strlen(buffer));
}

static PyObject* EMatrix_richcompare(EMatrix* self, PyObject* other, int op)
{
	if (!PyObject_TypeCheck(other, self->ob_base.ob_type)) {
		PyErr_SetString(PyExc_TypeError, "Argument must be EMatrix type.");
		return NULL;
	}

	switch (op) {
	case Py_EQ:
		return PyBool_FromLong(EVSpace_Matrix_eq((EMatrix*)self, (EMatrix*)other));
	case Py_NE:
		return PyBool_FromLong(EVSpace_Matrix_ne((EMatrix*)self, (EMatrix*)other));
	default:
		Py_RETURN_NOTIMPLEMENTED;
	}
}

PyDoc_STRVAR(ematrix_doc, "Euclidean matrix object used to operate on or rotate a euclidean vector.");

static PyTypeObject EMatrixType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	.tp_name = "pyevspace.EMatrix",
	.tp_doc = ematrix_doc,
	.tp_basicsize = sizeof(EMatrix),
	.tp_itemsize = 0,
	.tp_flags = Py_TPFLAGS_DEFAULT,
	.tp_new = PyType_GenericNew,
	.tp_init = (initproc)EMatrix_init,
	.tp_methods = EMatrix_Methods,
	.tp_str = (reprfunc)EMatrix_str,
	.tp_as_number = &EMatrix_NBMethods,
	.tp_richcompare = (richcmpfunc)EMatrix_richcompare,
};

PyDoc_STRVAR(evspace_doc, "Module library for a Euclidean vector space with a vector and matrix type as well as necessary methods to use them.");

static PyModuleDef EVSpacemodule = {
	PyModuleDef_HEAD_INIT,
	.m_name = "pyevspace",
	.m_doc = evspace_doc,
	.m_size = -1,
};

// todo: can we document all the methods for the IDE?
PyMODINIT_FUNC
PyInit_pyevspace(void)
{
	PyObject* m = NULL;
	static void* EVSpace_API[EVSpace_API_pointers];
	PyObject* c_api_object = NULL;
	EVector* e1 = NULL, *e2 = NULL, *e3 = NULL;
	EMatrix* I = NULL;
	
	if (PyType_Ready(&EVectorType) < 0)
		return NULL;
	if (PyType_Ready(&EMatrixType) < 0)
		return NULL;

	// create e1 vector
	e1 = (EVector*)EVectorType.tp_new(&EVectorType, NULL, NULL);
	if (!e1)
		return NULL;
	e1->m_arr[0] = 1;
	if (PyDict_SetItemString(EVectorType.tp_dict, "e1", (PyObject*)e1) < 0)
		return NULL;
	Py_DECREF(e1);

	// create e2 vector
	e2 = (EVector*)EVectorType.tp_new(&EVectorType, NULL, NULL);
	if (!e2)
		return NULL;
	e2->m_arr[1] = 1;
	if (PyDict_SetItemString(EVectorType.tp_dict, "e2", (PyObject*)e2) < 0)
		return NULL;
	Py_DECREF(e2);

	// craete e3 vector
	e3 = (EVector*)EVectorType.tp_new(&EVectorType, NULL, NULL);
	if (!e3)
		return NULL;
	e3->m_arr[2] = 1;
	if (PyDict_SetItemString(EVectorType.tp_dict, "e3", (PyObject*)e3) < 0)
		return NULL;
	Py_DECREF(e3);

	// create identity matrix
	I = (EMatrix*)EMatrixType.tp_new(&EMatrixType, NULL, NULL);
	if (!I)
		return NULL;
	I->m_arr[0][0] = I->m_arr[1][1] = I->m_arr[2][2] = 1.0;
	if (PyDict_SetItemString(EMatrixType.tp_dict, "I", (PyObject*)I) < 0)
		return NULL;
	Py_DECREF(I);

	// create module
	m = PyModule_Create(&EVSpacemodule);
	if (!m)
		goto error;

	// add module level class functions
	if (PyModule_AddFunctions(m, EMatrix_ModuleMethods) < 0) {
		Py_DECREF(m);
		return NULL;
	}
	if (PyModule_AddFunctions(m, EVector_ModuleMethods) < 0) {
		Py_DECREF(m);
		return NULL;
	}

	// EVector 
	EVSpace_API[EVSpace_Vector_add_NUM]		= (void*)EVSpace_Vector_add;
	EVSpace_API[EVSpace_Vector_sub_NUM]		= (void*)EVSpace_Vector_sub;
	EVSpace_API[EVSpace_Vector_mult_NUM]	= (void*)EVSpace_Vector_mult;
	EVSpace_API[EVSpace_Vector_neg_NUM]		= (void*)EVSpace_Vector_neg;
	EVSpace_API[EVSpace_Vector_abs_NUM]		= (void*)EVSpace_Vector_abs;
	EVSpace_API[EVSpace_Vector_iadd_NUM]	= (void*)EVSpace_Vector_iadd;
	EVSpace_API[EVSpace_Vector_isub_NUM]	= (void*)EVSpace_Vector_isub;
	EVSpace_API[EVSpace_Vector_imult_NUM]	= (void*)EVSpace_Vector_imult;
	EVSpace_API[EVSpace_Vector_div_NUM]		= (void*)EVSpace_Vector_div;
	EVSpace_API[EVSpace_Vector_idiv_NUM]	= (void*)EVSpace_Vector_idiv;
	EVSpace_API[EVSpace_Vector_eq_NUM]		= (void*)EVSpace_Vector_eq;
	EVSpace_API[EVSpace_Vector_ne_NUM]		= (void*)EVSpace_Vector_ne;
	EVSpace_API[EVSpace_Vector_dot_NUM ]	= (void*)EVSpace_Vector_dot;
	EVSpace_API[EVSpace_Vector_cross_NUM]	= (void*)EVSpace_Vector_cross;
	EVSpace_API[EVSpace_Vector_mag_NUM]		= (void*)EVSpace_vector_mag;
	EVSpace_API[EVSpace_Vector_mag2_NUM]	= (void*)EVSpace_Vector_mag2;
	EVSpace_API[EVSpace_Vector_norm_NUM]	= (void*)EVSpace_Vector_norm;
	EVSpace_API[EVSpace_Vector_inorm_NUM]	= (void*)EVSpace_Vector_inorm;
	EVSpace_API[EVSpace_Vector_vang_NUM]	= (void*)EVSpace_Vector_vang;
	EVSpace_API[EVSpace_Vector_vxcl_NUM]	= (void*)EVSpace_Vector_vxcl;
	// EMatrix
	EVSpace_API[EVSpace_Matrix_add_NUM]		= (void*)EVSpace_Matrix_add;
	EVSpace_API[EVSpace_Matrix_sub_NUM]		= (void*)EVSpace_Matrix_sub;
	EVSpace_API[EVSpace_Matrix_multm_NUM]	= (void*)EVSpace_Matrix_multm;
	EVSpace_API[EVSpace_Matrix_multv_NUM]	= (void*)EVSpace_Matrix_multv;
	EVSpace_API[EVSpace_Matrix_multd_NUM]	= (void*)EVSpace_Matrix_multd;
	EVSpace_API[EVSpace_Matrix_neg_NUM]		= (void*)EVSpace_Matrix_neg;
	EVSpace_API[EVSpace_Matrix_iadd_NUM]	= (void*)EVSpace_Matrix_iadd;
	EVSpace_API[EVSpace_Matrix_isub_NUM]	= (void*)EVSpace_Matrix_isub;
	EVSpace_API[EVSpace_Matrix_imultm_NUM]	= (void*)EVSpace_Matrix_imultm;
	EVSpace_API[EVSpace_Matrix_imultd_NUM]	= (void*)EVSpace_Matrix_imultd;
	EVSpace_API[EVSpace_Matrix_div_NUM]		= (void*)EVSpace_Matrix_div;
	EVSpace_API[EVSpace_Matrix_idiv_NUM]	= (void*)EVSpace_Matrix_idiv;
	EVSpace_API[EVSpace_Matrix_eq_NUM]		= (void*)EVSpace_Matrix_eq;
	EVSpace_API[EVSpace_Matrix_ne_NUM]		= (void*)EVSpace_Matrix_ne;
	EVSpace_API[EVSpace_Matrix_det_NUM]		= (void*)EVSpace_Matrix_det;
	EVSpace_API[EVSpace_Matrix_trans_NUM]	= (void*)EVSpace_Matrix_trans;

	// create capsule
	c_api_object = PyCapsule_New((void*)EVSpace_API, "evspace._C_API", NULL);
	if (!c_api_object)
		goto error;

	// add capsule to module
	if (PyModule_AddObject(m, "_C_API", c_api_object) < 0)
		goto error;

	// add EVector to module
	Py_INCREF(&EVectorType);
	if (PyModule_AddObject(m, "EVector", (PyObject*)&EVectorType) < 0)
		goto error;

	// add EMatrix to module
	Py_INCREF(&EMatrixType);
	if (PyModule_AddObject(m, "EMatrix", (PyObject*)&EMatrixType) < 0)
		goto error;
		
	return m;

error:

	Py_DECREF(m);
	Py_XDECREF(c_api_object);
	Py_DECREF(&EVectorType);
	Py_DECREF(&EMatrixType);

	return NULL;
}