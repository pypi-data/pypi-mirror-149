# Rigid Body Transformation
# 
# Jin Cao <aihalop@gmail.com>
# 2019-12-2

import numpy as np
import unittest
import numbers
import operator

SMALL_NUMBER = 1e-10

skew_symmetric = lambda v: np.array([[   0., -v[2],  v[1]],
                                     [ v[2],    0., -v[0]],
                                     [-v[1],  v[0],   0.]])

class Vector2(object):
    '''Representing an object living in 2-dimensional Euclidean space.'''

    def __init__(self, x=0., y=0.):
        self._x = x
        self._y = y

    @staticmethod
    def identity(self):
        '''Return vector (0, 0) in 2-dimensional Euclidean space.'''
        return Vector2()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __iadd__(self, other):
        assert isinstance(other, Vector2)
        self._x += other.x
        self._y += other.y
        return self

    def __add__(self, other):
        if not isinstance(other, Vector2):
            raise ValueError("{} is not a type of Vector2".format(other))
        return Vector2(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        if not isinstance(other, Vector2):
            raise ValueError("{} is not a type of Vector2".format(other))
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if not isinstance(other, numbers.Number):
            raise ValueError("{} is not a valid number.".format(other))
        return Vector2(other * self.x, other * self.y)

    def __rmul__(self, other):
        if not isinstance(other, numbers.Number):
            raise ValueError("{} is not a valid number.".format(other))
        return Vector2(other * self.x, other * self.y)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            norm_difference = \
                np.linalg.norm((self.x - other.x, self.y - other.y))
            return norm_difference < SMALL_NUMBER
        return False

    def normalized(self):
        '''Return normalized vector2.'''
        return self * (1 / np.linalg.norm((self.x, self.y)))

    def norm(self):
        '''Return Euclidean distance of the vector2.'''
        return np.linalg.norm([self.x, self.y])

    def __repr__(self):
        return "Vector2(xy: ({}, {}))".format(self.x, self.y)


class Vector3(object):
    '''Representing an object living in 3-dimensional Euclidean space.'''

    def __init__(self, x=0., y=0., z=0):
        self._x = x
        self._y = y
        self._z = z

    @staticmethod
    def identity(self):
        '''Return vector (0, 0, 0) in 3-dimensional Euclidean space.'''
        return Vector3()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def __iadd__(self, other):
        assert isinstance(other, Vector3)
        self._x += other.x
        self._y += other.y
        self._z += other.z
        return self

    def __add__(self, other):
        if not isinstance(other, Vector3):
            raise ValueError("{} is not a type of Vector3".format(other))
        return Vector3(
            self.x + other.x, self.y + other.y, self.z + other.z
        )

    def __radd__(self, other):
        if not isinstance(other, Vector3):
            raise ValueError("{} is not a type of Vector3".format(other))
        return Vector3(
            self.x + other.x, self.y + other.y, self.z + other.z
        )

    def __mul__(self, other):
        if not isinstance(other, numbers.Number):
            raise ValueError("{} is not a valid number.".format(other))
        return Vector3(other * self.x, other * self.y, other * self.z)

    def __rmul__(self, other):
        if not isinstance(other, numbers.Number):
            raise ValueError("{} is not a valid number.".format(other))
        return Vector3(other * self.x, other * self.y, other * self.z)

    def __eq__(self, other):
        if isinstance(other, Vector3):
            norm_difference = np.linalg.norm(
                (self.x - other.x, self.y - other.y, self.z - other.z)
            )
            return norm_difference < SMALL_NUMBER
        return False

    def normalized(self):
        return self * (1 / np.linalg.norm((self.x, self.y, self.z)))

    def norm(self):
        return np.linalg.norm([self.x, self.y, self.z])

    def __repr__(self):
        return "Vector3(xyz: ({:.4f}, {:.4f}, {:.4f}))".format(self.x, self.y, self.z)
    

class AxisAngle(object):
    """Representing rotation in axis-angle."""
    def __init__(self, angle, axis):
        assert isinstance(axis, Vector3)
        self._angle = angle
        self._axis = axis

    def ToQuaternion(self):
        w = np.cos(self._angle * 0.5)
        v = np.sin(self._angle * 0.5) * self._axis.normalized()
        return Quaternion(w, v.x, v.y, v.z)
        

class Quaternion(object):
    def __init__(self, w=1., x=0., y=0., z=0.):
        self._scaler = w
        self._vector = Vector3(x, y, z)

    @staticmethod
    def identity():
        return Quaternion()

    def scalar(self):
        return self._scaler

    def vector(self):
        return np.array([self._vector.x, self._vector.y, self._vector.z])

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            scalar = self.scalar() * other.scalar() \
                - np.dot(self.vector(), other.vector())
            vector = self.scalar() * other.vector() \
                + other.scalar() * self.vector() \
                + np.cross(self.vector(), other.vector())
            return Quaternion(scalar, *vector)
        elif isinstance(other, numbers.Number):
            return Quaternion(
                self.w * other,
                self.x * other,
                self.y * other,
                self.z * other
            )
        elif isinstance(other, Vector3):
            conjugation = self \
                * Quaternion(0, other.x, other.y, other.z) \
                * self.conjugate()
            return Vector3(*conjugation.vector())
        else:
            raise ValueError(
                "Quaterion can not multiply a object of type {}"
                .format(type(other))
            )

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return Quaternion(
                self.w * other,
                self.x * other,
                self.y * other,
                self.z * other
            )
        else:
            raise ValueError(
                "An object of type {} multiply a quaternion is Not Defined."
                .format(type(other))
            )

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(
                self.w + other.w,
                self.x + other.x,
                self.y + other.y,
                self.z + other.z
            )
        elif isinstance(other, numbers.Number):
            return self + Quaternion(other, 0, 0, 0)
        else:
            raise ValueError(
                "The operation of adding a value of type"
                "{} to a quaternion is Not Defined."
                .format(type(other))
            )
        
    def __eq__(self, other):
        if isinstance(other, Quaternion):
            norm_difference = np.linalg.norm(
                (self.w - other.w,
                 self.x - other.x,
                 self.y - other.y,
                 self.z - other.z)
            )
            return norm_difference < SMALL_NUMBER
        return False

    def __repr__(self):
        return "Quaternion(wxyz: ({:.4f}, {:.4f}, {:.4f}, {:.4f}))".format(
            self.scalar(), *self.vector()
        )

    def inverse(self):
        return self.conjugate() * (1 / np.square(self.norm()))

    def matrix(self):
        v = self.vector()
        qv = np.reshape(v, (3, 1))
        R = (self.w * self.w - np.dot(v, v)) * np.identity(3) \
            + 2 * qv * qv.T + 2 * self.w * skew_symmetric(self.vector())
        return R

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    @property
    def w(self):
        return self._scaler
    
    @property
    def x(self):
        return self._vector.x

    @property
    def y(self):
        return self._vector.y

    @property
    def z(self):
        return self._vector.z

    def norm(self):
        return np.linalg.norm((self.w, self.x, self.y, self.z))
    
    def normalized(self):
        scale = 1. / self.norm()
        return Quaternion(
            self._w * scale,
            self._x * scale,
            self._y * scale,
            self._z * scale
        )

    def ToEuler(self):
        """The Euler angle representation of the corresponding rotation.

        Return (roll, pitch, yaw)
        """
        w, x, y, z = self.w, self.x, self.y, self.z
        roll = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x**2 + y**2))
        sinp = np.arcsin(2 * (w * y - z * x))
        pitch = np.copysign(np.pi / 2, sinp) \
            if abs(sinp) >= 1 else np.arcsin(sinp)
        yaw = np.arctan2(2 * (w * z + x * y), 1 - 2 * (y**2 + z**2))
        return (roll, pitch, yaw)


class Translation(Vector3):
    """Representing Translation by Vector3"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __add__(self, other):
        vector3 = super().__add__(other)
        if isinstance(other, Translation):
            return Translation(vector3.x, vector3.y, vector3.z)
        else:
            return vector3

    def __repr__(self):
        return "Translation({})".format(super().__repr__())


class Rotation(Quaternion):
    """Representing Rotation by Quaternion."""
    def __init__(self, *args, **kwargs):
        if "yaw" in kwargs and "roll" in kwargs and "pitch" in kwargs:
            quaternion = \
                AxisAngle(kwargs["roll"], Vector3(1, 0, 0)).ToQuaternion() \
                * AxisAngle(kwargs["pitch"], Vector3(0, 1, 0)).ToQuaternion() \
                * AxisAngle(kwargs["yaw"], Vector3(0, 0, 1)).ToQuaternion()
            super().__init__(
                quaternion.w, quaternion.x, quaternion.y, quaternion.z
            )
        elif "angle" in kwargs and "axis" in kwargs:
            quaternion = AxisAngle(
                kwargs["angle"], kwargs["axis"]).ToQuaterion()
            super().__init__(
                quaternion.w, quaternion.x, quaternion.y, quaternion.z
            )
        else:
            super().__init__(*args, **kwargs)

    def __mul__(self, other):
        if isinstance(other, Translation):
            translation = super().__mul__(other)
            return Translation(
                translation.x, translation.y, translation.z
            )
        elif isinstance(other, Rotation):
            quaternion = super().__mul__(other)
            return Rotation(
                quaternion.w, quaternion.x, quaternion.y, quaternion.z
            )
        else:
            return super().__mul__(other)

    def inverse(self):
        quaternion = super().inverse()
        return Rotation(
            quaternion.w, quaternion.x, quaternion.y, quaternion.z
        )

    def __repr__(self):
        return "Rotation({})".format(super().__repr__())


class Rigid(object):
    """Representing Rigid Transformation."""

    def __init__(self, translation=Translation(), rotation=Rotation()):
        self._translation = translation
        self._rotation = rotation

    def inverse(self):
        return Rigid(
            -1 * (self._rotation.inverse() * self._translation),
            self._rotation.inverse()
        )

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return self._rotation * other + self._translation
        elif isinstance(other, Rigid):
            return Rigid(
                self._rotation * other.translation + self._translation,
                self._rotation * other.rotation
            )
        else:
            raise ValueError(
                "A Rigid object can not multiply an object of type {}".format(
                    type(other))
            )
        
    def __rmul__(self, other):
        if not isinstance(other, Rigid):
            raise ValueError(
                "A Rigid object can not multiply an object of type {}".format(
                    type(other))
            )

    def __eq__(self, other):
        return self._rotation == other.rotation and \
            self._translation == other.translation

    @property
    def rotation(self):
        return self._rotation

    @property
    def translation(self):
        return self._translation

    def __repr__(self):
        return "Rigid({}, {})".format(self.translation, self.rotation)


class Rigid3(Rigid):
    """Representing Rigid Transformation living in SE(3)."""
    def __mul__(self, other):
        rigid = super().__mul__(other)
        if isinstance(other, Rigid3):
            return Rigid3(rigid.translation, rigid.rotation)
        else:
            return rigid

    def __repr__(self):
        return "Rigid3({}, {})".format(self.translation, self.rotation)


class Rigid2(Rigid):
    """Representing Rigid Transformation living in SE(2)."""
    def __init__(self, x=0, y=0, theta=0):
        super().__init__(
            Translation(x, y, 0.),
            Rotation(roll=0.0, pitch=0.0, yaw=theta)
        )

    @property
    def x(self):
        return self._translation.x

    @property
    def y(self):
        return self._translation.y
    
    @property
    def theta(self):
        roll, pitch, yaw = self._rotation.ToEuler()
        return yaw

    def inverse(self):
        _inverse = super().inverse()
        x, y = _inverse.translation.x, _inverse.translation.y
        roll, pitch, yaw = _inverse.rotation.ToEuler()
        return Rigid2(x, y, yaw)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            rigid = super().__mul__(
                Rigid(Translation(other.x, other.y, 0.), Rotation())
            )
            x, y = rigid.translation.x, rigid.translation.y
            return Vector2(x, y)
        elif isinstance(other, Rigid):
            rigid = super().__mul__(
                Rigid(Translation(other.x, other.y, 0.),
                      Rotation(roll=0., pitch=0., yaw=other.theta))
            )
            x, y = rigid.translation.x, rigid.translation.y
            roll, pitch, yaw = rigid.rotation.ToEuler()
            return Rigid2(x, y, yaw)
        else:
            raise ValueError(
                "A Rigid2 can not be multiplied by an object of type {}".format(
                    type(other))
            )

    def __repr__(self):
        return "Rigid2(x,y,theta: {:.4f}, {:.4f}, {:.4f})".format(self.x, self.y, self.theta)


class TestVector2(unittest.TestCase):
    def test_vector_plus(self):
        v1 = Vector2(1., 2.)
        v2 = Vector2(3., 4.)
        self.assertEqual(v1 + v2, Vector2(4., 6.))

    def test_vector_multiple(self):
        v = Vector2(2.0, 3.0)
        self.assertEqual(v * 4, Vector2(8.0, 12.0))

    def test_norm(self):
        self.assertEqual(Vector2(3., 4.).norm(), 5.0)

class TestVector3(unittest.TestCase):
    def test_vector_plus(self):
        v1 = Vector3(1., 1., 1.)
        v2 = Vector3(1., 2., 3.)
        v1 += v2
        self.assertEqual(v1 + v2, Vector3(3., 5., 7.))
        self.assertRaises(ValueError, operator.add, 1.0, v1)
        self.assertRaises(ValueError, operator.add, v1, 1.0)

    def test_vector_multiple(self):
        v = Vector3(1., 2., 3.)
        self.assertEqual(v * 2, Vector3(2., 4., 6.))
        self.assertEqual(3 * v, Vector3(3., 6., 9.))

    def test_norm(self):
        self.assertEqual(Vector3(2,3,6).norm(), 7)

class TestAngleAxis(unittest.TestCase):
    def test_angleaxis(self):
        axis_angle = AxisAngle(np.pi / 2, Vector3(0., 0., 2.))
        self.assertEqual(
            axis_angle.ToQuaternion(),
            Quaternion(0.7071067811865477, 0., 0., 0.7071067811865476))
        

class TestRigid2(unittest.TestCase):
    def setUp(self):
        self.A = Rigid2(1., 0., np.pi / 2)
        self.B = Rigid2(1., 0., 0.)

    def test_inverse(self):
        self.assertEqual(self.A * self.A.inverse(), Rigid())

    def test_multiply(self):
        self.assertEqual(self.A * self.B, Rigid2(1., 1., np.pi / 2.))

    def test_multiply_vector(self):
        rigid2 = Rigid2(2., 1., np.pi / 2)
        vector = Vector2(1.0, 0.)
        self.assertEqual(rigid2 * vector, Vector2(2.0, 2.0))

class TestRotation(unittest.TestCase):
    def setUp(self):
        self.rotation = Rotation(roll=0.0, pitch=0.0, yaw=0.575)

    def test_rotation(self):
        self.assertAlmostEqual(self.rotation.w, 0.9589558)
        self.assertAlmostEqual(self.rotation.z, 0.2835557)

    def test_inverse(self):
        self.assertEqual(self.rotation.inverse() * self.rotation,
                         Quaternion.identity())


class TestRigid(unittest.TestCase):
    def setUp(self):
        self.A = Rigid(Translation(1., 0., 0.),
                       Rotation(roll=0., pitch=0., yaw=np.pi / 2))
        self.B = Rigid(Translation(1., 0., 0.),
                       Rotation(1.0, 0., 0., 0.))
        self.C = Rigid(Translation(0., 1., 0.),
                       Rotation(roll=0., pitch=0., yaw=np.pi / 4))

    def test_multiply(self):
        T_AB = self.A * self.B
        self.assertEqual(T_AB.translation, Translation(1., 1., 0.))
        self.assertEqual(
            T_AB.rotation, Rotation(roll=0., pitch=0., yaw=np.pi / 2))
        T_AC = self.A * self.C
        self.assertEqual(T_AC.translation, Translation(0., 0., 0.))
        self.assertEqual(
            T_AC.rotation,
            Rotation(roll=0., pitch=0., yaw=(np.pi / 2 + np.pi / 4)))

    def test_multiply_vector(self):
        T = Rigid(Translation(1., 1., 1.), Rotation(roll=0., pitch=0., yaw=np.pi / 2))
        vector = Translation(1., 0., 1.)
        self.assertEqual(T * vector, Translation(1., 2., 2.))
        
    def test_inverse(self):
        self.assertEqual(self.A.inverse() * self.A, Rigid())

    def test_exception(self):
        invalid_float_value = 1.0
        self.assertRaises(ValueError, lambda: self.A * invalid_float_value)
        self.assertRaises(ValueError, lambda: invalid_float_value * self.A)


class TestQuaternion(unittest.TestCase):
    def setUp(self):
        self.q45 = AxisAngle(np.pi / 4, Vector3(0., 0., 1.)).ToQuaternion()
        self.q90 = AxisAngle(np.pi / 2, Vector3(0., 0., 1.)).ToQuaternion()
        self.v = Vector3(1., 0., 0.)
        self.q1234 = Quaternion(1, 2, 3, 4)

    def test_initialization(self):
        identity = Quaternion()
        self.assertTupleEqual(
            (identity.w, identity.x, identity.y, identity.z),
            (1.0, 0.0, 0.0, 0.0)
        )

    def test_multiple(self):
        self.assertEqual(self.q45 * self.q45, self.q90)
        self.assertEqual(self.q90 * self.v, Vector3(0., 1., 0.))
        self.assertEqual(2. * Quaternion(1., 2., 3., 4.),
                         Quaternion(2., 4., 6., 8.))
        self.assertRaises(ValueError, lambda: self.q45 * "invalid type")
        self.assertRaises(ValueError, lambda: [1., 0., 0.] * self.q90)
        self.assertRaises(ValueError, lambda: self.v * self.q90)

    def test_addition(self):
        q = Quaternion(1, 0, 0, 0) + Quaternion(0, 0, 1, 0)
        self.assertTupleEqual((q.w, q.x, q.y, q.z), (1, 0, 1, 0))
        q_and_scaler = Quaternion(0, 0, 0, 0) + 1
        self.assertTupleEqual(
            (q_and_scaler.w, q_and_scaler.x, q_and_scaler.y, q_and_scaler.z),
            (1, 0, 0, 0)
        )

        self.assertRaises(ValueError, lambda: q + "invalid type")

    def test_conjugate(self):
        qc = self.q1234.conjugate()
        self.assertTupleEqual((qc.w, qc.x, qc.y, qc.z), (1, -2, -3, -4))

    def test_norm(self):
        self.assertAlmostEqual(self.q1234.norm(), 5.4772, 4)

    def test_inverse(self):
        q = self.q1234.inverse() * self.q1234
        i = Quaternion.identity()
        self.assertTupleEqual(
            (q.w, q.x, q.y, q.z),
            (i.w, i.x, i.y, i.z)
        )

    def test_matrix(self):
        diff_norm = np.linalg.norm(
            np.reshape(self.q90.matrix(), 9) - np.array([0., -1., 0.,
                                                       1., 0., 0.,
                                                       0., 0., 1.]))
        self.assertAlmostEqual(diff_norm, 0.)


if __name__=="__main__":
    unittest.main(exit=False)
