import bpy
import boxx
import numpy as np


class StereoCam:
    def __init__(self, main_cam, pose_Rt, K=None, hw=None):
        """
        if K is None, K = mian_cam's K

        if pose_RT is int or float, mean x
        """
        import bpycv

        self.bpycv = bpycv

        self.main = main_cam
        self.cam = self.bpycv.duplicate(self.main)
        self.cam.name = self.main.name + "_stereo"
        pose_Rt = np.array(pose_Rt)
        if pose_Rt.size == 1:
            _pose_Rt = np.eye(4)[:3]
            _pose_Rt[0][-1] = pose_Rt
            pose_Rt = _pose_Rt
        self.pose_Rt = pose_Rt

        self.hw = (
            bpy.context.scene.render.resolution_y,
            bpy.context.scene.render.resolution_x if hw is None else hw,
        )
        if K is None:
            K = np.array(self.bpycv.get_cam_intrinsic(self.main))
        else:
            self.bpycv.set_cam_intrinsic(self.cam, K, hw)

        self.K = K
        self.inv_K = np.linalg.inv(K)
        self.T_main_to_stereo = np.linalg.inv(self.bpycv.homo_coord(pose_Rt))
        self.set_pose()

    def set_pose(self):
        self.bpycv.set_pose_in_cam(
            self.cam, self.bpycv.T_bcam2cv[:3, :3] @ self.pose_Rt, self.main
        )

    def render_image(self):
        self.set_pose()
        old_cam = bpy.context.scene.camera
        bpy.context.scene.camera = self.cam
        image = self.bpycv.render_image()
        bpy.context.scene.camera = old_cam
        return image

    def get_disparity(self, depth):
        """
        depth of main
        """
        hw = boxx.Vector(depth.shape)
        ys, xs = np.mgrid[: hw[0], : hw[1]]
        depth_mask = depth > 0
        xys_in_main = np.array([xs, ys, np.ones_like(xs)])[:, depth_mask].T
        xyzs_in_main = np.dot(xys_in_main * depth[depth_mask, None], np.linalg.inv(K).T)
        xyzs_in_stereo = np.dot(
            bpycv.homo_coord(xyzs_in_main), self.T_main_to_stereo.T
        )[:, :3]
        depth_in_stereo = xyzs_in_stereo[:, 2]
        xy_in_stereo_ = (
            np.dot(xyzs_in_stereo, self.K.T)[:, :2] / depth_in_stereo[..., None]
        )
        xy_in_stereo = xy_in_stereo_.round(0).astype(np.int32)

        in_hw_mask = (
            (xy_in_stereo >= 0).all(1)
            & (xy_in_stereo[:, 0] < hw.w)
            & (xy_in_stereo[:, 1] < hw.h)
        )
        # out_hw_mask = (xy_in_stereo<0).any(1) | (xy_in_stereo[:, 0] >= hw.w)| (xy_in_stereo[:,1] >= hw.h)

        _xys, inverse = np.unique(xy_in_stereo, axis=0, return_inverse=1)
        idxs = np.arange(depth_in_stereo.size)
        not_occlude_mask = np.zeros_like(depth_in_stereo, dtype=bool)
        for i in range(len(_xys)):
            same_point_mask = inverse == i
            idx = idxs[same_point_mask][np.argmin(depth_in_stereo[same_point_mask])]
            not_occlude_mask[idx] = True

        matched_mask = np.zeros_like(depth_mask)
        matched_mask[depth_mask] = in_hw_mask & not_occlude_mask

        disparity = xys_in_main[:, :2] / xy_in_stereo
        # TODO TBD

    def remove(self):
        self.bpycv.remove_obj(self.cam)


with boxx.impt("/home/dl/megvii/project/ai_asrs/stereo_depth/tools"):
    from calibration_stereo import CalibrationStereo


class CalibrationStereoBlender(CalibrationStereo):
    def __init__(self, Rt, K, hw, K2=None):
        import cv2

        K1 = K
        K2 = K if K2 is None else K2
        D1 = np.zeros((1, 5))
        D2 = np.zeros((1, 5))
        xy = tuple(hw[::-1])
        R, T = Rt[:3, :3], Rt[:3, 3:] * 1000
        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(K1, D1, K2, D2, xy, R, T)
        self.data = dict(K1=K1, D1=D1, R1=R1, K2=K2, D2=D2, R2=R2, xy=xy, R=R, T=T)
        self._set_map()

    @classmethod
    def from_StereoCam(cls, stereo):
        cs = cls(
            stereo.pose_Rt,
            np.array(stereo.bpycv.get_cam_intrinsic(stereo.main)),
            stereo.hw,
            stereo.K,
        )
        return cs
