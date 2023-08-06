pro gclean,gstruc,gstruc2,htmin=htmin

; This program cleans the v=0 region and noise from a
; structure of gaussians
;
; This program assumes the following:
; 1.) A noise model of:
;     ht < -0.01 * sig + 0.3
; 2.) The v=0 region has two wide components
; 3.) The v=0 region might have thin gaussian
;     components as well.
; Any other gaussians are kept.
;

if n_params() eq 0 then begin
  print,'Syntax - gclean,gstruc,gstruc2,htmin=htmin'
  return
endif

gstruc2 = gstruc

if not keyword_set(htmin) then htmin=0.

; REMOVE NOISE GAUSSIANS
; ht < -0.01 * sig + 0.3, noise!
gd = where(gstruc2.par(0) gt -0.03*gstruc2.par(2)+0.3, ngd)
gstruc2 = gstruc2(gd)

; REMOVE LOW AMPLITUDE GAUSSIANS
;if (htmin gt 0.) then begin
;  gd2 = where(gstruc2.par(0) gt htmin, ngd2)
;  gstruc2 = gstruc2(gd2)
;endif

; REMOVE V=0 GAUSSIANS

; getting the v=0 region
ind0 = where(abs(gstruc2.par(1)) lt 30.,nind0)
mncen = mean(gstruc2(ind0).par(1))
stdcen = stdev(gstruc2(ind0).par(1))
cenminth = mncen-2.*stdcen
cenmaxth = mncen+2.*stdcen

;ind1 = where(gstruc2.par(1) gt cenminth and gstruc2.par(1) lt cenmaxth, nind1)

lmax = max(gstruc2.lon)
lmin = min(gstruc2.lon)
bmax = max(gstruc2.lat)
bmin = min(gstruc2.lat)
nl = (lmax-lmin)*2.+1.
nb = (bmax-bmin)*2.+1.

for i=0,nb-1 do begin

  ilat = bmin + 0.5*i

  for j=0,nl-1 do begin

    ilon = lmin + 0.5*j

    cur = where(gstruc2.lon eq ilon and gstruc2.lat eq ilat $
                and gstruc2.par(1) gt cenminth and gstruc2.par(1) lt cenmaxth, ncur)

    ; we've got some
    if ncur gt 0 then begin

      ipar = (gstruc2(cur).par)(*)
      npar = n_elements(ipar)

      ; getting the foreign gaussians
      area = garea(ipar)
      si = sort(area)
      bdpar = (gstruc2(cur(si)).par)(*)
      ;bdpar = ipar
      ng = npar/3

      ; remove first two
      if ng eq 1 then rem = [cur(0)]
      if ng gt 1 then rem = [cur(0:1)]
      ;if ng eq 1 then remove,cur(0),gstruc2
      ;if ng gt 1 then remove,cur(0:1),gstruc2

      ; removing thin gaussians
      if ng gt 2 then begin

        sigmin = 5.
        htmin = 0.0
  
        for k=2,ng-1 do begin
          kpar = gstruc2(cur(k)).par
          if (kpar(0) lt htmin) or (kpar(2) lt sigmin) then rem = [rem,cur(k)]
          ;if kpar(0) lt 0.3 or kpar(2) lt 5. then remove,cur(k),gstruc2
        end

      end

      ; removing gaussians
      ;print,gstruc2(rem).par(1)
      npts = n_elements(gstruc2)
      indarr = lindgen(npts)
      remove,rem,indarr
      gstruc2 = gstruc2(indarr)
      ;remove,rem,gstruc2

    end ; ncur > 0

    ;stop

  end ; for j

end ; for i

;stop

end
