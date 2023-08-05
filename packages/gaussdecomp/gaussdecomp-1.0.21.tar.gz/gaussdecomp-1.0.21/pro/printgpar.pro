pro printgpar,par,sigpar,ngauss,rms,noise,chisq,iter,status

; Printing the gaussian parameters
;
;  INPUT
;   par      Array of gaussian parameters
;   sigpar   Array of errors of gaussian parameters
;   ngauss   Number of gaussians
;   rms      RMS of gaussian fit
;   noise    Noise level
;   chisq    Chi squared of gaussian fit
;   iter     Number of iterations
;   status   Status of fitting procedure
;
;  OUTPUT
;   None
;
; Created by David Nidever April 2005

if n_params() eq 0 then begin
  print,'Syntax - printgpar,par,sigpar,ngauss,iter,chisq,rms,noise,status'
  return
endif

npar = n_elements(par)
if not keyword_set(ngauss) then ngauss = n_elements(par)/3
if not keyword_set(sigpar) then sigpar = fltarr(npar)
if ngauss*3 gt npar then ngauss=npar/3
orig_ngauss = ngauss

; printing the results
print,'----------------------------------------------------------'
print,' #       Height         Center         Width       Area'
print,'----------------------------------------------------------'
for i=0,ngauss-1 do begin
  ipar = par(i*3:i*3+2)
  isigpar = sigpar(i*3:i*3+2)
  iarea = garea(ipar)
  print,' ',strtrim(i+1,2),'   ',$
     stringize(ipar(0),ndec=2,len=6),' (',stringize(isigpar(0),sigfig=2,len=4),')  ',$
     stringize(ipar(1),ndec=2,len=6),' (',stringize(isigpar(1),sigfig=2,len=4),')  ',$
     stringize(ipar(2),ndec=2,len=6),' (',stringize(isigpar(2),sigfig=2,len=4),')  ',$
     stringize(iarea(0),ndec=2,len=6)
end
print,'----------------------------------------------------------'
if keyword_set(iter) then print,'N Iter = ',strtrim(iter,2)
if keyword_set(chisq) then print,'ChiSq = ',stringize(chisq,sigfig=3)
if keyword_set(rms) then print,'RMS = ',stringize(rms,sigfig=3)
if keyword_set(noise) then print,'Noise = ',stringize(noise,sigfig=3)
if keyword_set(status) then if status lt 0 then print,'Status = ',strtrim(status,2),'   NOT SUCCESSFUL'
print,''

ngauss = orig_ngauss
;stop

end
