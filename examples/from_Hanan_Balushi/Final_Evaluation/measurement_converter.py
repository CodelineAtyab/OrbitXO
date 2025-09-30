import logging

logger = logging.getLogger('measurement_api.converter')

class MeasurementConverter:
    """
    Converts measurement input strings into lists of total values for each package.
    
    Rules:
    - '_' (underscore) = 0
    - 'a' to 'z' = 1 to 26
    - 'z' cannot stand alone - must be combined with the next character
    - Multiple characters are added together for numbers > 26
    """
    
    def __init__(self):
        self.char_to_value = self._create_char_mapping()
    
    def _create_char_mapping(self):
        """Create character to value mapping"""
        mapping = {'_': 0}
        # a=1, b=2, ..., z=26
        for i, char in enumerate('abcdefghijklmnopqrstuvwxyz', start=1):
            mapping[char] = i
        return mapping
    
    def _decode_number(self, input_string, start_index):
        """
        Decode a number starting at start_index.
        Returns (number_value, next_index)
        
        Rules:
        - 'z' must be followed by another character, add their values
        - Non-'z' character terminates the number
        """
        if start_index >= len(input_string):
            raise ValueError("Unexpected end of input")
        
        total = 0
        i = start_index
        
        while i < len(input_string):
            char = input_string[i]
            
            if char not in self.char_to_value:
                raise ValueError(f"Invalid character: '{char}'")
            
            value = self.char_to_value[char]
            
            if char == 'z':
                # 'z' must be combined with the next character
                i += 1
                if i >= len(input_string):
                    raise ValueError("'z' cannot be at the end of input - must be followed by another character")
                
                next_char = input_string[i]
                if next_char not in self.char_to_value:
                    raise ValueError(f"Invalid character after 'z': '{next_char}'")
                
                next_value = self.char_to_value[next_char]
                total += value + next_value
                i += 1
                
                # If next_char was not 'z', the number terminates
                if next_char != 'z':
                    break
                # If next_char was 'z', continue (it will be processed in next iteration)
            else:
                # Non-'z' character terminates the number
                total += value
                i += 1
                break
        
        return total, i
    
    def _parse_input(self, input_string):
        """
        Parse the input string into packages.
        Each package: count + values
        """
        if not input_string:
            raise ValueError("Input string is empty")
        
        packages = []
        i = 0
        
        while i < len(input_string):
            # Decode the count
            count, i = self._decode_number(input_string, i)
            logger.debug(f"Package count: {count}")
            
            # Read 'count' number of values
            values = []
            for _ in range(count):
                if i >= len(input_string):
                    raise ValueError(f"Unexpected end of input while reading values (expected {count} values, got {len(values)})")
                
                value, i = self._decode_number(input_string, i)
                values.append(value)
                logger.debug(f"Value: {value}")
            
            package_total = sum(values)
            packages.append(package_total)
            logger.debug(f"Package total: {package_total} from values: {values}")
        
        return packages
    
    def convert(self, input_string):
        """
        Main conversion method.
        
        Args:
            input_string: The measurement input string
            
        Returns:
            List of total values for each package
        """
        logger.info(f"Converting: {input_string}")
        
        try:
            result = self._parse_input(input_string)
            logger.info(f"Conversion result: {result}")
            return result
        except Exception as e:
            logger.error(f"Conversion error: {str(e)}")
            raise ValueError(f"Conversion failed: {str(e)}")