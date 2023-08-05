pro gaussfitter,l,b,par0,sigpar,rms,noise,v,spec,resid,noplot=noplot,$
                ngauss=ngauss,noprint=noprint,color=color,$
                vmax=vmax,vmin=vmin,inpar=inpar,inv=inv,$
                inspec=inspec,diag=diag

;  This program tries to do gaussian analysis 
;  on HI spectra.
;
;  INPUT
;   l       galactic longitude
;   b       galactic latitude
;   inpar   initial guess of parameters
;   inv     use input velocity array 
;   inspec  use input spectrum array
;
;  OUTPUT
;   par0    final parameters
;   v       array of velocities
;   spec    spectrum
;   resid   the residuals
;   rms     the rms of the residuals
;
;  KEYWORDS
;   /noplot   don't plot anything
;   /noprint  don't print anything
;   /diag     diagnostic printing and plotting
;   /color    use color
;   vmin      the minimum velocity to use
;   vmax      the maximum velocity to use
;
;   Written by D. Nidever, April 2005

; Start time
gt0 = systime(1)

; No Inputs
if n_params() eq 0 then begin
  print,'Syntax - gaussfitter,l,b,par0,sigpar,rms,noise,v,spec,resid,noplot=noplot,$'
  print,'                     ngauss=ngauss,noprint=noprint,color=color,$'
  print,'                     vmax=vmax,vmin=vmin,inpar=inpar,inv=inv,$'
  print,'                     inspec=inspec,diag=diag'
  return
endif

; Default position
if n_elements(l) eq 0 or n_elements(b) eq 0 then begin
  l = 295.
  b = -60.
endif

; Original printing
if not keyword_set(noprint) then begin
  print,'Fitting Gaussians to the HI spectrum at (',stringize(l,ndec=1),',',stringize(b,ndec=1),')'
endif

; Getting the HI spectrum
if n_elements(inv) gt 0 and n_elements(inspec) gt 0 then begin
  v = inv
  spec = inspec
endif else begin
  rdhispec,l,b,spec,v
endelse

; Estimating the noise
hinoise,v,spec,noise
;noise = 0.05
noise_orig = noise
;noise = noise > 0.070    ; 0.070 K is the average noise level

; Velocity range
;vmin = -50.  ;-100
;vmax = 50.   ;100
if not keyword_set(vmin) then vmin=min(v)
if not keyword_set(vmax) then vmax=max(v)
gd = where(v ge vmin and v le vmax,ngd)
old_v = v
old_spec = spec
spec = spec(gd)
v = v[gd]
dv = v[1]-v[0]
vmin = min(v)
vmax = max(v)
dum = closest(0,v,ind=vindcen)

; Initalizing Some Parameters
if keyword_set(par0) then par0=0
npts = n_elements(v)
rms = 999999.
rms0 = 999999.
count = 0
npar0 = 0
y = spec
endflag = 0
addt0 = systime(1)

;goto,HERE

; TRYING THE FIRST GUESS PARAMETERS
if (n_elements(inpar) gt 1) then begin

  print,'Using First Guess Parameters'
  orig_inpar = inpar

  gremove,inpar,v,y   ; removing bad ones
  gremdup,inpar,v     ; removing the duplicates

  ;letting everything float
  gfit,v,y,inpar,finpar,sigpar,rms,chisq,iter,residuals,status,weights=weights,$
         noise=noise,rt=rt1

  ;stop

  gremove,finpar,v,y   ; removing bad ones
  gremdup,finpar,v     ; removing the duplicates

  ;stop

endif  ; inpar exists

;stop

; ADDING GAUSSIANS

; One gaussian added per loop
WHILE (endflag ne 1) do begin

  if not keyword_set(noprint) then print,'count = ',stringize(count,ndec=0)

  ; Using the initial guess
  ;if keyword_set(finpar) then if finpar(0) ne -1 then par0=finpar
  if n_elements(finpar) gt 1 then par0=finpar
  if keyword_set(par0) then npar0 = n_elements(par0)

  ; Getting the Residuals
  if keyword_set(par0) then begin
    th = gfunc(v,par0)
    if th(0) ne 999999. then resid = y-th else resid=y
  endif else resid = y

  ; Smoothing the data
  ;smresid1 = savgolsm(resid, [1,1,2])
  smresid4 = savgolsm(resid, [4,4,2])
  smresid16 = savgolsm(resid, [16,16,2])
  if (npts gt 61) then smresid30 = savgolsm(resid, [30,30,2]) $
    else smresid30 = fltarr(npts)
  if (npts gt 101) then smresid50 = savgolsm(resid, [50,50,2]) $
    else smresid50 = fltarr(npts)
  if (npts gt 201) then smresid100 = savgolsm(resid, [100,100,2]) $
    else smresid100 = fltarr(npts)
  maxy = max(resid)

  ;stop

  ; Setting up some arrays
  rmsarr = fltarr(200)+999999. 
  pararr = fltarr(200,3)+999999.
  ;rmsarr = 0
  ;pararr = 0
  gcount = 0

  ; Looping through the different smoothed spectra
  for s = 0,4 do begin 

    ; Getting the right smoothed spectrum
    case s of
    0: smresid = smresid4
    1: smresid = smresid16
    2: smresid = smresid30
    3: smresid = smresid50
    4: smresid = smresid100
    endcase

    ; Getting maxima
    gpeak1,smresid,(5*noise > 0.5*maxy),maxarr
    if maxarr(0) eq -1 then gpeak1,smresid,(5*noise > 0.1*maxy),maxarr
    if maxarr(0) eq -1 then gpeak1,smresid,5.*noise,maxarr
    if maxarr(0) eq -1 then gpeak1,smresid,3.*noise,maxarr
    if maxarr(0) eq -1 then gpeak1,smresid,2.*noise,maxarr
    ngd = n_elements(maxarr)

    ; if there are any peaks check them out
    if maxarr(0) ne -1 then begin

      ; Looping through the peaks and fitting them
      ; to the proper residual spectrum
      ; only one gaussian, plus a line
      for i=0,ngd-1 do begin

        maxi = maxarr(i)

        ; getting guess and fitting it
        gest,v,smresid,maxi,par2,gind=gind

        ; only do it if there is a good range
        if gind(0) ne -1 then begin
          par2s = [par2,0.01,0.01]
          gfit,v(gind),smresid(gind),par2s,fpar2s,sigpar2,rms2,chisq2,iter,residuals,$
               status,weights=weights,noise=noise,rt=rt2,func='gdev1'
          fpar2 = fpar2s(0:2)
          ;rms = sqrt(total(weights*(resid-gfunc(v,fpar2))^2.)/(npts-1))
          rms = stdev(resid-gfunc(v,fpar2))
        endif else begin
          rms = 999999.
          fpar2 = par2*0.+999999.
        endelse

        ; Adding to the rms and par arrays
        rmsarr(gcount) = rms
        pararr(gcount,*) = fpar2
 
        ;stop
        ;wait,0.5

        gcount = gcount + 1

      endfor ; for i

    endif  ; if there are any peaks for this smoothed spectrum

  endfor ; for s, looping through smoothed spectra

  ; Only taking the good rms
  gdrms = where(rmsarr ne 999999.,ngdrms)

  ;stop

  ; No good ones
  if ngdrms eq 0 then begin
    if (count eq 0) then begin
      endflag = 1
      par0 = -1
      goto,BOMBEND
    endif else begin
      endflag = 1
      goto,BOMB
    endelse
  endif
  rmsarr = rmsarr(gdrms)
  pararr = pararr(gdrms,*)
  pararr = (transpose(pararr))(*)  ; change to the normal mode

  ;stop

  ; Removing bad gaussians
  gremove,pararr,v,y

  ; Removing the duplicates
  gremdup,pararr,v

  ; No good ones
  if n_elements(pararr) lt 2 then begin
    endflag = 1
    goto,BOMB
  endif


  ; Setting up some arrays
  n = n_elements(pararr)/3
  rmsarr2 = fltarr(n)
  if keyword_set(par0) then pararr2 = fltarr(n,n_elements(par0)+3)
  if not keyword_set(par0) then pararr2 = fltarr(n,3)
  sigpararr2 = pararr2*0.

  if not keyword_set(noprint) then print,strtrim(n,2),' gaussian candidates'


  ; Looping through the candidates that are left
  ;  allowing everything to float
  for i=0,n-1 do begin

    ipar = pararr(3*i:3*i+2)

    if keyword_set(par0) then par = [par0,ipar]
    if not keyword_set(par0) then par = ipar

    ; Letting everything float
    gfit,v,y,par,fpar,sigpar,rms,chisq,iter,residuals,status,weights=weights,$
         noise=noise,rt=rt5

    npar = n_elements(fpar)
    rmsarr2(i) = rms
    ;pararr2(3*i:3*i+2) = fpar(npar-3:npar-1)
    pararr2(i,*) = fpar
    sigpararr2(i,*) = sigpar

    ; Giagnostic plotting and printing
    if keyword_set(diag) then begin
      gplot,v,y,fpar
      printgpar,fpar,sigpar,n_elements(fpar)/3,rms,noise,chisq,iter,status
      wait,1.5
    endif

    ;stop

  endfor  ;for i, looping through candidates

  ;stop

  ; Adding the gaussian with the lowest rms
  gdi = first_el(where(rmsarr2 eq min(rmsarr2) and rmsarr2 ne 999999, ngdi))
  ;gdi = first_el(minloc(rmsarr2))
  if ngdi gt 0 then begin
    par0 = reform(pararr2(gdi,*))
    npar0 = n_elements(par0)
    sigpar = sigpararr2(gdi,*)
    rms = rmsarr2(gdi)

    sigpar00 = sigpar
    rms00 = rms
  endif

  ; Plot what we've got so far
  ;if not keyword_set(noplot) then gplot,v,spec,par0

  ; Printing the parameters
  ;ngauss = n_elements(par0)/3
  if not keyword_set(noprint) and rms ne 999999 then $
    printgpar,par0,sigpar,ngauss,rms,noise,chisq,iter

  ; Ending Criteria
  drms = (rms0-rms)/rms0
  if (rms le noise) then endflag = 1
  if (rms ge rms0) then endflag = 1
  if (drms lt 0.02) then endflag = 1

  ; Saving the rms
  rms0 = rms

  count = count + 1

  BOMB:

  ;stop

ENDWHILE ; while (endflag ne 1)
if not keyword_set(noprint) then print,'END Addition of Gaussians ',systime(1)-addt0,' sec'

;stop

; Saving the results of the fit
sigpar00 = sigpar
rms00 = rms
;chisq00 = chisq
;iter00 = iter
;status00 = status

; Plot what we've got so far
if not keyword_set(noplot) then gplot,v,spec,par0

; Printing the parameters
ngauss = n_elements(par0)/3
if not keyword_set(noprint) then printgpar,par0,sigpar00,ngauss,rms,noise

;stop


; REMOVING GAUSSIANS

; Removing bad gaussians
gremove,par0,v,y

; Removing the duplicates
gremdup,par0,v

;stop

; None left - End
if par0(0) eq -1 then goto,BOMBEND

; Sorting the gaussians by area
orig_par0 = par0
ngauss = n_elements(par0)/3
par0 = gsort(par0)

; See if removing the smallest (in area) gaussian changes much

count = 0
ngauss = n_elements(par0)/3

orig_par0 = par0
nrefit = ceil(ngauss/2)
;rmsarr = fltarr(nrefit)
;pararr = fltarr(nrefit,n_elements(par0)-3)

weights = dblarr(npts)+1.
rms0 = sqrt(total(weights*(spec-gfunc(v,par0))^2.)/(npts-1))

; Looping through the smallest 1/2
for i=0,nrefit-1 do begin

  ig = ngauss-i-1
  tpar = par0

  ; Remove the gaussian in question
  remove,[0,1,2]+ig*3,tpar

  ; Finding the best fit
  gfit,v,y,tpar,fpar,sigpar,rms,chisq,iter,residuals,status,weights=weights,noise=noise,rt=rt5

  ;gplot,v,spec,fpar
  ;printgpar,fpar,sigpar,ngauss-1,rms,noise,chisq,iter,status

  drms = rms-rms0
  ; remove the gaussian
  if (drms/rms0 lt 0.02) then begin
    par0=fpar
    rms0 = sqrt(total(weights*(spec-gfunc(v,par0))^2.)/(npts-1))

    ; saving the results of the fit
    ;  without this gaussian
    sigpar00 = sigpar
    rms00 = rms
    chisq00 = chisq
    iter00 = iter
    status00 = status
  endif

  ;print,rms,drms/rms0
  ;print,'time = ',rt5

  ;stop

end  ;for i


; Removing bad gaussians
gremove,par0,v,y

; Run it one last time for the final values
gfit,v,y,par0,fpar,sigpar,rms,chisq,iter,residuals,status,weights=weights,noise=noise,rt=rt5
par0 = fpar
ngauss = n_elements(par0)/3

;print,systime(1)-t0

;stop

; Final Results
ngauss = n_elements(par0)/3
if not keyword_set(noplot) then gplot,v,spec,par0
if not keyword_set(noprint) then printgpar,par0,sigpar,ngauss,rms,noise,chisq

; Printing the total time
if not keyword_set(noprint) then print,'Total time = ',stringize(systime(1)-gt0,ndec=2)

BOMBEND:

; No gaussians found
if par0(0) eq -1 then begin
  sigpar = par0*0.-1
  rms = stdev(spec)
endif

spec = old_spec
v = old_v

;stop

end
