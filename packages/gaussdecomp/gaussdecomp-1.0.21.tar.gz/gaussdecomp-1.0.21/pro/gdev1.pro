function gdev1,par,dp,x=x,y=y,err=err,th=th,noderiv=noderiv

;  This function drives gaussfunc
;  and returns the deviates
;
;  INPUT
;   par       Gaussian parameters
;   x=x       Array of X values
;   y=y       Array of Y values
;   err=err   Array of error values
;   /noderiv  Don't return the derivative
;
;  OUTPUT
;   dev       Deviants of observed and theoretical points dev=(y-th)/err
;   th        Theoretical Y values
;   dp        Derivative of deviants with the parameters (optional)
;
; When there are problems in this program it returns:
;  dev = x*0.+999999.
;  dp = x*0.+999999.
;
; Created by David Nidever April 2005

nx = n_elements(x)
ny = n_elements(y)
nerr = n_elements(err)

; Bad Input Values
if (n_params() eq 0) or (nx eq 0) or (ny eq 0) or (nerr eq 0) or $
     ((nx ne ny) or (nx ne nerr)) then begin
  print,'Syntax - dev=gdev1(par,dp,X=x,Y=y,ERR=err,th=th,/noderiv)'
  if nx gt 0 then dev = x*0.+999999. else dev=999999.
  if not keyword_set(nodev) then dp = dev
  return,dev
endif

if n_params() gt 1 then noderive=0

th = gfunc1(x,par,dp,noderiv=noderiv)
return,(y-th)/err

end
