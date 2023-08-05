pro gfit,x,y,par,fpar,perror,rms,chisq,iter,resid,status,parinfo=parinfo,$
         weights=weights,noise=noise,rtime=rtime,func=func

;  This program fits gaussians to a spectrum, given initial estimates
;
;  INPUT
;   x         Array of X values
;   y         Array of Y values
;   par       Initial guess parameters
;  
;  OPTIONAL INPUTS
;   parinfo=parinfo  Structure of parameter limits (defaults set by "setlimits.pro")
;   func = func      Name of function to use (default: "gdev")
;   noise = noise    Noise level
;
;  OUTPUT
;   fpar      Final parameters
;   perror    Errors of final parameters
;   rms       RMS of final fit
;   chisq     Chi squared of final fit
;   iter      Number of iterations
;   resid     Residuals of spectrum - final fit
;   status    Status
;   rtime     Run time in seconds
;   noise     Noise level
;   weights   Weights of points (currently all set to 1)
;
;   If there are any problems this program returns:
;    fpar = par
;    perror = par*0.+999999.
;    rms = 999999.
;    chisq = 999999.
;    iter = 0
;    resid = y*0.
;    weights = x*0.+1.
;
;   Written by D. Nidever, April 2005

If n_params() eq 0 then begin
  print,'Syntax - gfit,x,y,par,fpar,perror,rms,chisq,iter,resid,status,'
  print,'              parinfo=parinfo,func=func,weights=weights,noise=noise,'
  print,'              rtime=rtime'
  return
endif

t0=systime(1)
npts = n_elements(x)
npar = n_elements(par)

; function to use
if not keyword_set(func) then func='gdev'

; getting the noise level
if not keyword_set(noise) then hinoise,x,y,noise

;setting the limits
if not keyword_set(parinfo) then setlimits,x,y,par,parinfo
parcheck,x,y,par,badflag

; checking for bad stuff
;if npts lt 3 then badflag = 1
;if npts lt npar then badflag = 1
;if npar lt 3 then badflag = 1

; Initial parameters are okay
if badflag eq 0 then begin

  ;weights = (noise/(noise+0.00216*y))^2.   ; using Haud's method, pg. 91, eg.5
  weights = dblarr(npts)+1.
  ;weights = dblarr(npts)+0.01
  ftol = 1d-6
  fa = {x:x,y:y,err:weights}

  p = mpfit(func, par, functargs=fa, perror=perror,niter=iter,status=status,$
             bestnorm=chisq, /quiet, parinfo=parinfo, dof=dof, autoderivative=0,$
             ftol=ftol)   ;,/nocatch)


  ; Bad stuff happend in MPFIT (status = 0, or -16)
  if (status lt 1) then begin
    if status eq 0 then print,'BAD INPUT PARAMETERS'
    if status eq -16 then print,'BAD INPUT PARAMETERS'

    fpar = par
    perror = par*0.+999999.
    rms = 999999.
    chisq = 999999.
    iter = 0
    resid = y*0.
    weights = x*0.+1.

    rtime = systime(1)-t0
    return
  endif

  ;if status eq 0 then print,'BAD INPUT PARAMETERS'
  ;if status eq 0 then stop
  ;if not keyword_set(perror) then stop

  ; scaled sigpars (from mpfit.pro)
  sigpar = perror * sqrt(chisq/dof)

  fpar = p   ;final parameters

  ; total resid
  result = gfunc(x,fpar)
  resid = y-result
  ;rms = sqrt(total(resid^2)/(npts-n_elements(fpar)-1))
  rms = sqrt(total(weights*resid^2.)/(npts-1))  ; using Haud's method, pg. 92, eg.6


; Problems with the initial parameters
endif else begin
  fpar = par
  perror = par*0.+999999.
  rms = 999999.
  chisq = 999999.
  iter = 0
  resid = y*0.
  weights = x*0.+1.
endelse

rtime = systime(1)-t0

;stop

end
