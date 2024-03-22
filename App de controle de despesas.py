import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

class Despesa:
    def __init__(self, descricao, valor, vencimento, lista):
        self.descricao = descricao
        self.valor = valor
        self.vencimento = vencimento
        self.pago = False
        self.lista = lista

class GerenciadorDespesasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Despesas Pessoais")

        self.listas_despesas = {}
        self.lista_atual = None

        self.mes_label = tk.Label(root, text="Mês:")
        self.mes_label.grid(row=0, column=0)
        self.mes_entry = tk.Entry(root)
        self.mes_entry.grid(row=0, column=1)
        self.mes_entry.bind("<Return>", self.criar_lista)

        self.descricao_label = tk.Label(root, text="Descrição:")
        self.descricao_label.grid(row=1, column=0)
        self.descricao_entry = tk.Entry(root)
        self.descricao_entry.grid(row=1, column=1)

        self.adicionar_despesa_button = tk.Button(root, text="Adicionar Despesa", command=self.adicionar_despesa)
        self.adicionar_despesa_button.grid(row=1, column=2)

        self.lista_combobox = ttk.Combobox(root, state="readonly")
        self.lista_combobox.grid(row=0, column=2)
        self.atualizar_combobox()

        self.adicionar_lista_button = tk.Button(root, text="Adicionar Lista", command=self.criar_lista)
        self.adicionar_lista_button.grid(row=0, column=3)

        self.exibir_listas_button = tk.Button(root, text="Exibir Listas", command=self.exibir_listas)
        self.exibir_listas_button.grid(row=1, column=3)

        self.valor_label = tk.Label(root, text="Valor:")
        self.valor_label.grid(row=2, column=0)
        self.valor_entry = tk.Entry(root)
        self.valor_entry.grid(row=2, column=1)

        self.sair_button = tk.Button(root, text="Sair", command=root.quit)
        self.sair_button.grid(row=2, column=2)

    def criar_lista(self, event=None):
        mes = self.mes_entry.get()
        if mes:
            if mes not in self.listas_despesas:
                self.listas_despesas[mes] = []
                self.atualizar_combobox()
                self.mes_entry.delete(0, tk.END)
                messagebox.showinfo("Sucesso", f"Lista para o mês {mes} criada com sucesso!")
            else:
                messagebox.showerror("Erro", f"Lista para o mês {mes} já existe.")
        else:
            messagebox.showerror("Erro", "Por favor, insira o nome do mês.")

    def atualizar_combobox(self):
        self.lista_combobox["values"] = list(self.listas_despesas.keys())

    def exibir_listas(self):
        exibir_listas_window = tk.Toplevel(self.root)
        exibir_listas_window.title("Listas de Despesas")

        listas_despesas_listbox = tk.Listbox(exibir_listas_window, height=10, width=50)
        listas_despesas_listbox.pack()

        for mes in self.listas_despesas:
            listas_despesas_listbox.insert(tk.END, mes)

        listas_despesas_listbox.bind("<Double-Button-1>", lambda event: self.exibir_lista(event, listas_despesas_listbox))

    def exibir_lista(self, event, listas_despesas_listbox):
        try:
            index = listas_despesas_listbox.curselection()[0]
            mes = listas_despesas_listbox.get(index)
            if mes in self.listas_despesas:
                exibir_despesas_window = tk.Toplevel(self.root)
                exibir_despesas_window.title(f"Lista de Despesas - {mes}")

                lista_despesas_text = tk.Text(exibir_despesas_window, height=10, width=60)
                lista_despesas_text.pack()

                def atualizar_lista():
                    lista_despesas_text.delete(1.0, tk.END)
                    for despesa in self.listas_despesas[mes]:
                        cor = "green" if despesa.pago else "red" if despesa.vencimento < datetime.today().date() else "black"
                        lista_despesas_text.insert(tk.END, f" {despesa.descricao} - R${despesa.valor} - {despesa.vencimento.strftime('%d/%m/%y')}\n", cor)
                        lista_despesas_text.tag_add("color", "insert-1c", "insert")
                        lista_despesas_text.tag_config("color", foreground=cor)

                exibir_despesas_window.protocol("WM_DELETE_WINDOW", exibir_despesas_window.destroy)
                exibir_despesas_window.bind("<Visibility>", lambda event: atualizar_lista())
                atualizar_lista()

            else:
                messagebox.showerror("Erro", "Lista selecionada não existe.")
        except IndexError:
            pass

    def adicionar_despesa(self):
        descricao = self.descricao_entry.get()
        valor = self.valor_entry.get()
        mes = self.lista_combobox.get()

        if descricao and valor and mes:
            try:
                valor = float(valor)
                vencimento = datetime.today().date()
                despesa = Despesa(descricao, valor, vencimento, mes)
                self.listas_despesas[mes].append(despesa)
                self.exibir_lista(None, self.lista_combobox)
                messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorDespesasApp(root)
    root.mainloop()
