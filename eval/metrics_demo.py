import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

true_img = data.camera().astype(np.float64)   # sample grayscale image, values 0-255
noise = np.random.normal(0, 15, true_img.shape)
pred_img = np.clip(true_img + noise, 0, 255)  # "prediction" = image + noise

mae = np.mean(np.abs(true_img - pred_img))
rmse = np.sqrt(np.mean((true_img - pred_img) ** 2))
psnr = peak_signal_noise_ratio(true_img, pred_img, data_range=255)
ssim = structural_similarity(true_img, pred_img, data_range=255)

print(f"MAE : {mae:.2f}  (lower is better)")
print(f"RMSE: {rmse:.2f}  (lower is better)")
print(f"PSNR: {psnr:.2f} dB  (higher is better)")
print(f"SSIM: {ssim:.3f}  (1 is perfect)")

fig, ax = plt.subplots(1, 2, figsize=(8, 4))
ax[0].imshow(true_img, cmap="gray"); ax[0].set_title("True")
ax[1].imshow(pred_img, cmap="gray"); ax[1].set_title("Predicted")
plt.show()