ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP2()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_760 = (MDL_COMPLEXI*MDL_I94A233)/4.000000D+00-(MDL_COMPLEXI
     $ *MDL_I94A323)/4.000000D+00-(MDL_COMPLEXI*MDL_I95A233)/4.000000D
     $ +00+(MDL_COMPLEXI*MDL_I95A323)/4.000000D+00
      END
