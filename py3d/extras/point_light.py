from py3d.geometry.sphere import SphereGeometry
from py3d.material.surface import SurfaceMaterial
from py3d.core_ext.mesh import Mesh


class PointLightHelper(Mesh):
    def __init__(self, point_light, size=0.1, line_width=1):
        color = point_light.color
        geometry = SphereGeometry(
            radius=size,
            theta_segments=2,
            phi_segments=4)
        material = SurfaceMaterial(
            property_dict={
                "baseColor": color,
                "wireframe": True,
                "doubleSide": True,
                "lineWidth": line_width,
            }
        )
        super().__init__(geometry, material)
