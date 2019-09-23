from math import cos, sin, atan


class flat_plate(object):
    """
    Flat plate.

    Parameters
    ----------
    x : float
        Chord position, from 0 to 1
    """

    # def __init__(self):
    #     pass

    def camber_line(self, x):
        """
        Returns the (local) camber line of the airfoil.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        z = 0

        return z

    def camber_gradient(self, x):
        """
        Returns the (local) camber gradient of the airfoil.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        dz = 0

        return dz

    def thickness(self, x):
        """
        Returns the (local) half-thickness distribution.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        t = 0

        return t

    def upper_surface(self, x):
        """
        Returns the position of the upper surface.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        xu = x
        yu = 0

        return xu, yu

    def lower_surface(self, x):
        """
        Returns the position of the lower surface.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        xl = x
        yl = 0

        return xl, yl


class NACA4(object):
    """
    4-digit NACA airfoils generator. Calculates the camber line,
    its gradient, (half) thickness distribution and the position
    of both lower and upper surfaces. Default values are set for
    the NACA 2412.

    Reference:
    [1] http://airfoiltools.com/airfoil/naca4digit
    [2] NACA Report 824, pp 262

    Parameters
    ----------
    x : float
        Chord position, from 0 to 1
    M, P, T: integer
             Digits on the NACA designation
             M - maximum camber (divided by 100)
             P - maximum camber position (divided by 10)
             T - thickness referred to the chord (divided by 100)
                 approximately at 30% of the chord
    """

    def __init__(self, M=2, P=4, T=12):
        self.M = M/100
        self.P = P/10
        self.T = T/100

        if M < 0 or M > 9.5:
            msg = 'Max camber M should be within [0, 9.5]'
            raise ValueError(msg)

        if P < 0 or P > 9:
            msg = 'Max camber position P should be within [0, 9]'
            raise ValueError(msg)

        if T < 0 or T > 40:
            msg = 'Thickness T should be within [0, 40]'
            raise ValueError(msg)

    def camber_line(self, x):
        """
        Returns the (local) camber line of the airfoil.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        M = self.M
        P = self.P

        if x < P:
            z = (M/P**2) * x * (2*P - x)
        else:
            z = (M / (1 - P)**2) * (1 - 2*P + x * (2*P - x))

        return z

    def camber_gradient(self, x):
        """
        Returns the (local) camber gradient of the airfoil.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        M = self.M
        P = self.P

        if x < P:
            dz = (2*M/P**2) * (P - x)
        else:
            dz = (2*M / (1 - P)**2) * (P - x)

        return dz

    def thickness(self, x):
        """
        Returns the (local) half-thickness distribution.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        T = self.T

        # Values for a t=20% airfoil
        a0, a1, a2, a3, a4 = 0.2969, -0.126, -0.3516, 0.2843, -0.1015

        # Half thickness (corrected from t=20% values)
        t = (T/0.2) * (a0*x**0.5 + x*(a1 + x*(a2 + x*(a3 + x*a4))))

        return t

    def upper_surface(self, x):
        """
        Returns the position of the upper surface.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        theta = atan(self.camber_gradient(x))

        xu = x - self.thickness(x) * sin(theta)
        yu = self.camber_line(x) + self.thickness(x) * cos(theta)

        return xu, yu

    def lower_surface(self, x):
        """
        Returns the position of the lower surface.
        """

        if x < 0 or x > 1:
            msg = 'Argument x should be within [0, 1]'
            raise ValueError(msg)

        theta = atan(self.camber_gradient(x))

        xl = x + self.thickness(x) * sin(theta)
        yl = self.camber_line(x) - self.thickness(x) * cos(theta)

        return xl, yl
