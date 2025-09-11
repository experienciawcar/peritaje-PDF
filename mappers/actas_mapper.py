from pathlib import Path

class ActasMapper:
    def __init__(self, data: dict):
        self.data = data

    def map(self) -> dict:
        return {
            "id": self.data.get("id"),
            "operation_date": self.data.get("operation_date"),
            "operation_hour": self.data.get("operation_hour"),
            "title": self._build_title(self.data.get("operation_type")),
            "client": self._build_client(self.data.get("client", {})),
            "vehicle": self._build_vehicle(self.data.get("vehicle", {})),
            "inventary": self._build_inventary(self.data.get("inventary", {})),
            "user": self._build_user(self.data.get("user", {})),
            "observations": self.data.get("observations", ""),
            "gasoil_level": self._build_gasoil_level(self.data.get("gasoil_level", "empty")),
        }
        
    def _build_title(self, operation_type):
        if operation_type == 1:
            return "recepcion"
        return "entrega"

    def _build_vehicle(self, vehicle_data):
        return {
            "plate": vehicle_data.get("plate"),
            "year": vehicle_data.get("year"),
            "brand": vehicle_data.get("brand"),
            "reference": vehicle_data.get("reference"),
            "color": vehicle_data.get("color"),
            "mileage": vehicle_data.get("mileage"),
            "soat_date": vehicle_data.get("soat_date"),
            "rtm_date": vehicle_data.get("rtm_date"),
            "body_work": vehicle_data.get("body_work"),
        }
        
    def _build_client(self, client_data):
        return {
            "signature": client_data.get("signature"),
            "full_name": client_data.get("full_name"),
            "document_number": client_data.get("document_number"),
            "email": client_data.get("email"),
            "address": client_data.get("address"),
            "phone_number": client_data.get("phone_number"),
        }

    def _build_inventary(self, inventary_data):
        return {
            "soat": "check" if inventary_data.get("soat") else "uncheck",
            "property_card": "check" if inventary_data.get("property_card") else "uncheck",
            "rtm": "check" if inventary_data.get("rtm") else "uncheck",
            "rugs": "check" if inventary_data.get("rugs") else "uncheck",
            "compressor": "check" if inventary_data.get("compressor") else "uncheck",
            "radio": "check" if inventary_data.get("radio") else "uncheck",
            "taxes": "check" if inventary_data.get("taxes") else "uncheck",
            "folders": "check" if inventary_data.get("folders") else "uncheck",
            "manuals": "check" if inventary_data.get("manuals") else "uncheck",
            "lug_wrench_crossbar": "check" if inventary_data.get("lug_wrench_crossbar") else "uncheck",
            "jack": "check" if inventary_data.get("jack") else "uncheck",
            "lug_wrench": "check" if inventary_data.get("lug_wrench") else "uncheck",
            "road_kit": "check" if inventary_data.get("road_kit") else "uncheck",
            "key_duplicate": "check" if inventary_data.get("key_duplicate") else "uncheck",
            "spare_tire": "check" if inventary_data.get("spare_tire") else "uncheck"
        }
        
    def _build_user(self, user_data):
        return {
            "full_name": user_data.get("full_name"),
            "email": user_data.get("email"),
            "signature": user_data.get("signature"),
        }

    def _build_gasoil_level(self, gasoil_level):
        BASE_DIR = Path(__file__).resolve().parent.parent
        if gasoil_level == "good":
            image_to_use = "https://storage.googleapis.com/course-gcp-2024-images/publics/Tanque_4_4.png"
        elif gasoil_level == "acceptable":
            image_to_use = "https://storage.googleapis.com/course-gcp-2024-images/publics/Tanque_3_4.png"
        elif gasoil_level == "regular":
            image_to_use = "https://storage.googleapis.com/course-gcp-2024-images/publics/Tanque_2_4.png"
        else:
            image_to_use = "https://storage.googleapis.com/course-gcp-2024-images/publics/Tanque_1_4.png"

        return image_to_use
