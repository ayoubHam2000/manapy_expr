# prevent multiplication between operation (dx * dx) or (dy * dx) or (dy * grad) ...
# prevent multiplication between variables and operation to variables dx(u) * v
# prevent multiplication between variables v * u
# multiplication of different variables
# can't do multiplication between partial operations
# can't do multiplication between variables or operation of variable

# prevent that the order of (grad, laplace) go further then 1
# prevent that the order of (dx, dt, dz, dt) fo further then 2
# prevent that the operations (dx, dt, dz, dt, grad, laplace) from having an expression, they can only hold a variable
# prevent operation (dx, dy, dz, dt, grad, laplace) on constant

# Equation
# specify dimension
# auto order
# auto get set of variables
# auto has grad
# auto has laplace

# generate many symbols
# insure that symbols names are unique

?????????????????????????

#is grad(a) * a allowed
#is multi variable is allowed
#control the number of variables ?? u + v ?? laplace(u) + grad(v) ??
#prevent dt * dt

################# next

#add a node to an expression 
#is there is any operation that should be added
#is there is any math function that should be added
#generate code
