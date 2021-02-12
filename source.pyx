cdef list stars = []
cdef double INTERVAL = 0.001


cdef class Star:    # Classes are struct inside. 
                    # Declared with "cdef" but accessible with Python
    cdef double x,y,vx,vy,ax,ay,m
    cdef str name

    def __cinit__(self, double x, double y, double vx, double vy, double m, str name):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m
        self.name = name
        self.ax = 0
        self.ay = 0
        stars.append(self)

    cdef update_speed(self):
        cdef double dirx, diry, r2, a
        cdef Star star # Need to define star, so I can use Star.x later
        
        for star in stars:
            if star == self:
                continue

            # Calculate acceleration 
            dirx = star.x - self.x
            diry = star.y - self.y
            r2 = dirx**2 + diry**2
            a = star.m / r2 #Using natural units so G=1

            # Project acceleration into components
            if dirx == 0:
                self.ax = 0
            elif dirx > 0:
                self.ax = a * (((r2 - diry**2 )/ r2) ** 0.5)
            else:
                self.ax = a * (((r2 - diry**2 )/ r2) ** 0.5) * (-1)

            if diry == 0:
                self.ay = 0
            elif diry > 0:
                self.ay = a * (((r2 - dirx**2 )/ r2) ** 0.5)
            else:
                self.ay = a * (((r2 - dirx**2 )/ r2) ** 0.5) * (-1)

            # Update speeds
            self.vx += INTERVAL * self.ax
            self.vy += INTERVAL * self.ay


    cdef update_position(self):
        self.x += self.vx * INTERVAL
        self.y += self.vy * INTERVAL


cpdef update_star_positions(int steps):
    """ Go over stars and update their positions 
    Returns x,y,sizes,names """
    cdef int i
    cdef list x = []
    cdef list y = []
    cdef list sizes = []
    cdef list names = []
    cdef Star star

    for i in range(steps):
        for star in stars:
            star.update_speed()
        for star in stars:
            star.update_position()

    for star in stars:            
        x.append(star.x)
        y.append(star.y)
        sizes.append(star.m)
        names.append(star.name)

    return x, y, sizes, names


cpdef get_arrows():
    cdef Star star
    cdef list lvx = []
    cdef list lvy = []
    cdef list lax = []
    cdef list lay = []
    for star in stars:
        lvx.append(star.vx)
        lvy.append(star.vy)
        lax.append(star.ax)
        lay.append(star.ay)
    return lvx, lvy, lax, lay