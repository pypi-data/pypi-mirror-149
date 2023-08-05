function gfunc1,x,par,dp,noderiv=noderiv

;  This function makes a gaussian with power terms

; each gaussian has 3 parameters height, center, width
; one extra for a constant offset
; 
;
;  INPUT
;   x         Array of X values
;   par       Gaussian parameters
;   /noderiv  Don't return the derivative
;
;  OUTPUT
;   th        Theoretical Y values
;   dp        Derivative of gaussian with the parameters (optional)
;
; When there are problems in this program it returns:
;  th = x*0.+999999.
;  dp = x*0.+999999.
;
; Created by David Nidever April 2005

npar = n_elements(par)
npts = n_elements(x)
npow = npar-3

; Bad Input Values
if (n_params() eq 0) or (npts eq 0) or (npar lt 3) then begin
  print,'Syntax - dev=gfunc1(x,par,dp,/noderiv)'
  if npts gt 0 then th = x*0.+999999. else th = 999999.
  if not keyword_set(noderive) then dp = th
  return,th
endif

ipar = par(0:2)
y = ipar(0)*exp(-0.5*((x-ipar(1))/ipar(2))^2.)

; adding power terms
if npow gt 0 then for i=0,npow-1 do y = y + par(i+3)*x^float(i)

; computing partial derivatives with respect to the parameters
if not keyword_set(noderiv) then begin
  dp = fltarr(npts,npar)
  ipar = par(0:2)
  ; height
  dp(*,0) = exp(-0.5*((x-ipar(1))/ipar(2))^2.)
  ; center
  dp(*,1) = dp(*,0)*ipar(0)*(x-ipar(1))/ipar(2)^2.
  ;  width
  dp(*,2) = dp(*,0)*ipar(0)*((x-ipar(1))^2.)/ipar(2)^3.

  for i=0,npow-1 do dp(*,i+3) = x^float(i)

endif

;stop

return,y

end
