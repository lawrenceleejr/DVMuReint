ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP3()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_6 = -G
      GC_7 = MDL_COMPLEXI*G
      GC_92 = MDL_COMPLEXI*MDL_G__EXP__2*MDL_I124A33+MDL_COMPLEXI
     $ *MDL_G__EXP__2*MDL_I125A33
      GC_737 = -(MDL_COMPLEXI*G*MDL_I84A33)-MDL_COMPLEXI*G*MDL_I85A33
      GC_739 = -(MDL_COMPLEXI*G*MDL_I84A36)-MDL_COMPLEXI*G*MDL_I85A36
      GC_745 = MDL_COMPLEXI*G*MDL_I84A63+MDL_COMPLEXI*G*MDL_I85A63
      END
