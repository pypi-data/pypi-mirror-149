pro setlimits,x,y,par,parinfo,ngauss=ngauss

;  This program sets limits for the gaussian parameters.
;
;  INPUT
;   x        Array of x values
;   y        Array of y values
;   par      Gaussian parameters
;
;  OUTPUT
;   parinfo  Structure of parameters limits for gfit.pro
;   ngauss   Number of gaussians
;
; When there are problems in the this program it returns:
;  parinfo = repliceate({limited:[0,0],limits:[0.,0.]},npar)
;  ngauss = 0.
; Not sure if these are the best things to return when there
;  are problems.
;
; Created by David Nidever April 2005

nx = n_elements(x)
ny = n_elements(y)
npar =  n_elements(par)
if not keyword_set(ngauss) then ngauss = npar/3

; Bad Input Values
if (n_params() eq 0) or (ngauss eq 0) or (npar eq 0) or (nx eq 0) or (ny eq 0) or $
     (nx ne ny) then begin
  print,'Syntax - setlimits,x,y,par,parinfo,ngauss=ngauss'
  if npar eq 0 then npar=1
  parinfo = replicate({limited:[0,0],limits:[0.,0.]},npar)
  ngauss = 0.
  return
endif

; Array limits
xmin = min(x)
xmax = max(x)
ymin = min(y)
ymax = max(y)

; Creating the Structure
parinfo = replicate({limited:[0,0],limits:[0.,0.]},npar)
flag = 0

; Setting limits
for i=0,ngauss-1 do begin

  ;height limits, must be greater than 0, le than height
  parinfo(3*i).limited(0:1) = [1,1]
  parinfo(3*i).limits(0:1) = [0.01,ymax*2.]

  ;center limits, must be within velocity bound, must be close to center
  parinfo(3*i+1).limited(0:1) = [1,1]
  parinfo(3*i+1).limits(0:1) = [xmin,xmax]

  ;width limits, must be greater than 0, less than half the xscale
  parinfo(3*i+2).limited(0:1) = [1,1]
  parinfo(3*i+2).limits(0:1) = [0.5,(xmax-xmin)*0.5]

end

; Constant offset, must be great than 0 and less than max height
if npar gt ngauss*3 then begin
  parinfo(ngauss*3).limited(0:1) = [1,1]
  parinfo(ngauss*3).limits(0:1) = [0.,ymax+0.1]
endif

;stop

end
