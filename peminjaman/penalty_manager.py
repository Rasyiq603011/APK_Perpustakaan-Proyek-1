import datetime

PENALTY_PER_DAY = 5000  # Denda per hari keterlambatan

def check_penalty(peminjaman_file, penalty_file):
    """
    Mengecek buku yang terlambat dikembalikan dan menghitung penalti.
    """
    today = datetime.date.today()
    updated_peminjaman = []
    penalties = []

    with open(peminjaman_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        book_title, borrow_date, return_date = line.strip().split(", ")
        return_date = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()

        if today > return_date:  # Jika sudah lewat batas waktu
            late_days = (today - return_date).days
            penalty_amount = late_days * PENALTY_PER_DAY
            penalties.append(f"{book_title}, {return_date}, {late_days}, {penalty_amount}")

        else:
            updated_peminjaman.append(line.strip())

    # Simpan ulang peminjaman.txt tanpa buku yang terlambat
    with open(peminjaman_file, "w") as file:
        for entry in updated_peminjaman:
            file.write(entry + "\n")

    # Simpan penalti ke penalty.txt
    with open(penalty_file, "a") as file:
        for penalty in penalties:
            file.write(penalty + "\n")

    return penalties

# Contoh pemanggilan
if __name__ == "__main__":
    penalties = check_penalty("../data/peminjaman.txt", "../data/penalty.txt")
    if penalties:
        print("Buku yang dikenakan penalti:")
        for penalty in penalties:
            print(penalty)
    else:
        print("Tidak ada keterlambatan.")
