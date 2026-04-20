// Khi trang load xong
document.addEventListener("DOMContentLoaded", () => {
    console.log("Trang đã load thành công!");

    // Demo: bắt sự kiện cho nút "Thêm mới" trong Admin
    const addBtn = document.querySelector(".add");
    if (addBtn) {
        addBtn.addEventListener("click", () => {
            alert("Chức năng thêm mới (demo)");
        });
    }

    // Demo: bắt sự kiện cho nút "Cập nhật" trong Teacher
    const updateBtns = document.querySelectorAll("button");
    updateBtns.forEach(btn => {
        if (btn.textContent.includes("Cập nhật")) {
            btn.addEventListener("click", () => {
                alert("Cập nhật điểm (demo)");
            });
        }
    });

    // Demo: bắt sự kiện đăng xuất
    const logoutLinks = document.querySelectorAll("a[href*='index.html']");
    logoutLinks.forEach(link => {
        link.addEventListener("click", () => {
            alert("Bạn đã đăng xuất (demo)");
        });
    });
});
