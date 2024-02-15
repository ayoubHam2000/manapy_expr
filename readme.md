#prevent multiplication between operation (dx * dx) or (dy * dx) or (dy * grad) ...
#prevent multiplication between variables and operation to variables dx(u) * v
#prevent multiplication between variables v * u
# prevent that the order of (grad, laplace) go further then 1
# prevent that the order of (dx, dt, dz, dt) fo further then 2
# prevent that the operations (dx, dt, dz, dt, grad, laplace) from having an expression, they can only hold a variable


#auto dimension
#auto order
#auto variables
#auto has grad
#auto has laplace
#generate many symbols
#insure that symbols names are unique

?????????????????????????

#control the number of variables ?? u + v ?? laplace(u) + grad(v) ??
#prevent dt * dt

#################next

#is there is any operation that should be added
#is there is any math function that should be added
#generate code