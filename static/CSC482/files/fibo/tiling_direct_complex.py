import cmath

class Solution:
    def numTilings(self, n: int) -> int:
        term1 = (
        (1/3) 
        - (1/354) * (1 + cmath.sqrt(3)*1j) * ((3481/2) - (177 * cmath.sqrt(177))/2)**(1/3)
        - ((1 - cmath.sqrt(3)*1j) * (1/2 * (59 + 3 * cmath.sqrt(177)))**(1/3)) / (6 * 59**(2/3))
    ) * (
        (2/3) 
        - (1/6) * (1 - cmath.sqrt(3)*1j) * ((43/2) - (3 * cmath.sqrt(177))/2)**(1/3)
        - (1/6) * (1 + cmath.sqrt(3)*1j) * (1/2 * (43 + 3 * cmath.sqrt(177)))**(1/3)
    )**n
    
        term2 = (
        (1/3) 
        - (1/354) * (1 - cmath.sqrt(3)*1j) * ((3481/2) - (177 * cmath.sqrt(177))/2)**(1/3)
        - ((1 + cmath.sqrt(3)*1j) * (1/2 * (59 + 3 * cmath.sqrt(177)))**(1/3)) / (6 * 59**(2/3))
    ) * (
        (2/3) 
        - (1/6) * (1 + cmath.sqrt(3)*1j) * ((43/2) - (3 * cmath.sqrt(177))/2)**(1/3)
        - (1/6) * (1 - cmath.sqrt(3)*1j) * (1/2 * (43 + 3 * cmath.sqrt(177)))**(1/3)
    )**n
    
        term3 = (
        1/59 * (59 + ((3481/2) - (177 * cmath.sqrt(177))/2)**(1/3) + (59/2 * (59 + 3 * cmath.sqrt(177)))**(1/3))
        * 3**(-n - 1) 
        * (2 + ((43/2) - (3 * cmath.sqrt(177))/2)**(1/3) + (1/2 * (43 + 3 * cmath.sqrt(177)))**(1/3))**n
    )
    
        result = term1 + term2 + term3
        result_real_part = result.real  # Extract the real part
        result_approx_int = int(round(result_real_part))  # Round to the nearest integer
        result_modulo = result_approx_int % (10**9 + 7)  # Apply modulo
    
        return result_modulo
