function garea,par,pow=pow,column=column

; This function returns the area of a gaussian given its parameters
; If multiple gaussians are given then it returns an array of the
; areas of the individual gaussians (not combined).
; The area of a gaussian is A = ht*wid*sqrt(2*pi)

if n_params() lt 1 then begin
  print,'Syntax - area = garea(par)'
  return,-1
endif

area = -1    ; default unless proven wrong
if par(0) eq -1 then goto,BOMB
if n_elements(pow) eq 0 then pow=1

npar = n_elements(par)
ngauss = npar/3
;area = fltarr(ngauss)
;for i=0.,ngauss-1 do area(i) = (par(i*3)^pow)*(par(i*3+2)/sqrt(pow))*sqrt(2.*!dpi)
area = (par[0:ngauss*3-1:3]^pow)*(par[2:ngauss*3-1:3]/sqrt(pow))*sqrt(2.0*!dpi)

BOMB:

if ngauss eq 1 then area=area(0)

; Output the column density
; N = 1.83e18 * Total(T_B(K))*dvel = 1.83e18 * area
if keyword_set(column) then area = area * 1.83d18

return,area

end
