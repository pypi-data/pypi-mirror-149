function gsort,par,dec=dec,si=si,cen=cen

; This program sorts an array of gaussian parameters in
; order of decreasing area (largest first)
;
;  INPUT
;   par        Array of gaussian parameters
;   /dec       Order in increasing order (smaller first)
;   /cen       Order by center
;   si         Array of indices sorted by newpar = par(si)
;
;  OUTPUT
;   newpar     Array of ordered gaussian parameters
;
; Created by David Nidever May 2005

npar = n_elements(par)

; Bad Input Values
if (n_params() eq 0) or (npar eq 0) then begin
  print,'Syntax - newpar = gsrot(par,/reverse)'
  return,-1
endif

; Not enough parameters
if (npar lt 3) then return,par

ngauss = npar/3
if not keyword_set(cen) then begin
  tsi = reverse(sort(garea(par)))
  if keyword_set(dec) then tsi = sort(garea(par))

  si = par*0
  for i=0,ngauss-1 do si(i*3:i*3+2) = tsi(i)*3+[0,1,2]
  newpar = par(si)

endif else begin
  pararr = fltarr(ngauss,3)
  for i=0,ngauss-1 do pararr(i,*) = par(i*3:i*3+2)
  si = sort(reform(pararr(*,1)))
  if keyword_set(dec) then si=reverse(si) 
  pararr = pararr(si,*)
  newpar = (transpose(pararr))(*)
endelse

return,newpar

end
