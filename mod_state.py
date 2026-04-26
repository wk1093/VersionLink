from collections import Counter

class ModState:
    def __init__(self, identifier):
        self.identifier = identifier
        self.supported_configs = set() # Set of (version, loader)

    def add_version(self, version, loader):
        self.supported_configs.add((version, loader))

    @staticmethod
    def analyze_compatibility(mod_list):
        if not mod_list:
            return None, []

        # 1. Try for perfect intersection
        intersection = mod_list[0].supported_configs.copy()
        for mod in mod_list[1:]:
            intersection &= mod.supported_configs

        if intersection:
            return list(intersection), []

        # 2. Fallback: Find the "Best Fit" (Most common version/loader pair)
        all_configs = []
        for mod in mod_list:
            all_configs.extend(list(mod.supported_configs))
        
        # Count occurrences of each (version, loader) pair
        counts = Counter(all_configs)
        best_fit_config, count = counts.most_common(1)[0]
        
        # Find who doesn't support the best fit
        incompatible = [
            mod.identifier for mod in mod_list 
            if best_fit_config not in mod.supported_configs
        ]

        return [best_fit_config], incompatible