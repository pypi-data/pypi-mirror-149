function gbetter,par1,rms1,noise1,par2,rms2,noise2

; This function tries to figure out if one gaussian
; analysis is better than another.
;
;  INPUT
;   par1    Gaussian Parameters of position 1
;   rms1    RMS of position 1
;   noise1  Noise level of position 1
;   par2    Gaussian Parameters of position 2
;   rms2    RMS of position 2
;   noise2  Noise level of position 2
;
;  OUTPUT
;   better  The function value is either:
;            1 - Second position better than the first
;            0 - First position better than the second
;           -1 - Any problems
;
; If the first one is better then it returns 0
; and if the second one is better it returns 1
;
; When this program has any problems is return:
;  better = -1
;
; Created by David Nidever April 2005

npar1 = n_elements(par1)
nrms1 = n_elements(rms1)
nnoise1 = n_elements(noise1)
npar2 = n_elements(par2)
nrms2 = n_elements(rms2)
nnoise2 = n_elements(noise2)

if (n_params() eq 0) or (npar1 eq 0) or (nrms1 eq 0) or (nnoise1 eq 0) or $
      (npar2 eq 0) or (nrms2 eq 0) or (nnoise2 eq 0) then begin
  print,'Syntax - better=gbetter(par1,rms1,noise1,par2,rms2,noise2)'
  return,-1
endif

better = -1   ; default unless proven wrong

; in case either one is -1 (bad)
if n_elements(par1) gt 0 and n_elements(par2) gt 0 then begin
  if (rms1 eq -1) and (rms2 ne -1) then better = 1
  if (rms1 ne -1) and (rms2 eq -1) then better = 0
  if (rms1 eq -1) and (rms2 eq -1) then better = -1
  if (rms1 eq -1) or (rms2 eq -1) then goto,BOMB
  if (n_elements(par1) lt 3) and (n_elements(par2) ge 3) then better = 1
  if (n_elements(par2) lt 3) and (n_elements(par1) ge 3) then better = 0
  if (n_elements(par1) lt 3) or (n_elements(par2) lt 3) then goto,BOMB
endif

if not keyword_set(par2) then goto,BOMB

drms1 = rms1-noise1
drms2 = rms2-noise2
n1 = n_elements(par1)/3
n2 = n_elements(par2)/3

; Clear cut, rms better, n equal or less
if (drms1 lt drms2) and (n1 le n2) then better = 0 
if (drms1 gt drms2) and (n1 ge n2) then better = 1

; rms same, n different
if (drms1 eq drms2) and (n1 le n2) then better = 0 
if (drms1 eq drms2) and (n1 gt n2) then better = 1

; mixed bag, lower rms but higher n
if (drms1 lt drms2) and (n1 gt n2) then begin
  ddrms = drms2-drms1
  ;rdrms = ddrms/mean([noise1,noise2])
  rdrms = ddrms/drms2   ; ratio compared to worse one
  dn = n1-n2

  better = 1  ; default
  if (dn eq 1) and (rdrms gt 0.2) then better = 0
  if (dn eq 2) and (rdrms gt 0.5) then better = 0
  if (dn eq 3) and (rdrms gt 1.0) then better = 0
  if (dn ge 4) and (rdrms gt 2.0) then better = 0

  ;stop

end

if (drms2 lt drms1) and (n2 gt n1) then begin
  ddrms = drms1-drms2
  ;rdrms = ddrms/mean([rms1,rms2])
  rdrms = ddrms/drms1    ; ratio compared to worse one
  dn = n2-n1

  better = 0  ; default
  if (dn eq 1) and (rdrms gt 0.2) then better = 1
  if (dn eq 2) and (rdrms gt 0.5) then better = 1
  if (dn eq 3) and (rdrms gt 1.0) then better = 1
  if (dn ge 4) and (rdrms gt 2.0) then better = 1

  ;stop

end

;stop

BOMB:

;stop

return,better

end
