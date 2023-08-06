pro gremdup,pararr,v

; This program removes gaussian parameters that
; are very similar to another one
;
;  INPUT
;   pararr  Array of parameters [ngauss*3]
;   v       Array of velocities
;
;  OUTPUT
;   pararr  Array of parameters with duplicate removed
;
; Created by David Nidever April 2005

npar = n_elements(pararr)
nv = n_elements(v)

; Bad Input Values
if (n_params() eq 0) or (npar eq 0) or (nv eq 0) then begin
  print,'Syntax - gremdup,pararr,v'
  return
endif

orig_pararr = pararr

n = n_elements(pararr)/3
vmin = min(v)
vmax = max(v)
dv = v(1)-v(0)
dum = closest(0,v,ind=vindcen)

; Removing "duplicates"

endflag = 0
i = 0

; Checking all N(N-1)/2 possible combinations
; First loop
WHILE (endflag eq 0) do begin

    n = n_elements(pararr)/3
    if i ge n-2 then goto,BOMB
    ;print,n,i
    ;if i lt 0 or i gt n-2 then stop
    ipar = pararr(3*i:3*i+2)
    ig = gfunc(v,ipar)
   
    endflag2 = 0
    j = i + 1

    ; Second loop
    while (endflag2 eq 0) do begin
      jpar = pararr(3*j:3*j+2)
      jg = gfunc(v,jpar)

      ; Use the narrowest range possible
      vlo = ( vmin > (ipar(1)-ipar(2)*3. < jpar(1)-jpar(2)*3.) )+0.5  ; just to be safe
      vhi = ( vmax < (ipar(1)+ipar(2)*3. > jpar(1)+jpar(2)*3.) )-0.5  ; just to be safe
      vran = vhi-vlo
      if finite(vran/dv+1.) eq 0 then stop
      ;print,vran/dv+1.
      ind = indgen(vran/dv+1.)+vindcen+vlo/dv

      ; Calculating the similarity
      ;sim = total( (ig-jg)^2. ) / ( total(ig^2.) + total(jg^2.) )
      sim = total( (ig(ind)-jg(ind))^2. )*dv / ( garea(ipar,pow=2) + garea(jpar,pow=2) )

      ;plot,v,ig
      ;oplot,v,jg,co=500
      ;print,total(ig^2.),total(jg^2.),total( (ig-jg)^2. )
      ;stop

      n = n_elements(pararr)/3
      if j eq n-1 then endflag2 = 1

      ; Similar gaussians, replace by single average
      if sim lt 0.1 then begin
         ;print,'TWO GAUSSIANS ARE VERY SIMILAR!!!'
         n = n_elements(pararr)/3
         ;pararr = [pararr(0:i,*),pararr((j+1) < (n-1):n-1,*)]
         ;pararr = [pararr(0:i*3+2),pararr( ((j+1) < (n-1))*3 : (n-1)*3+2 )]
         remove,[0,1,2]+3*j,pararr
         ; don't increment
         ;stop
      endif else begin
         ; increment to next
         j = j + 1
      endelse

      ;print,i,j,n_elements(pararr)/3,sim,endflag2
      ;stop

    end  ; for j
 
    BOMB:

    n = n_elements(pararr)/3
    if i ge n-2 then endflag = 1

    i = i + 1

  end  ;for i

;stop

end
