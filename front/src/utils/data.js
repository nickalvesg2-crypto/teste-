export function dataLocalISO(date = new Date()) {
  const ano = date.getFullYear();
  const mes = String(date.getMonth() + 1).padStart(2, '0');
  const dia = String(date.getDate()).padStart(2, '0');
  return `${ano}-${mes}-${dia}`;
}

export function chaveData(valor) {
  if (!valor) return '';
  return String(valor).slice(0, 10);
}

export function formatarHora(valor) {
  if (!valor) return '';
  return String(valor).slice(0, 5);
}

export function formatarDataCurta(valor) {
  const chave = chaveData(valor);
  if (!chave) return '';
  const [ano, mes, dia] = chave.split('-');
  return `${dia}/${mes}/${ano}`;
}

export function tituloDoDia(date = new Date()) {
  const dia = date.getDate();
  const mes = date.toLocaleDateString('pt-BR', { month: 'long' });
  return `Hoje, ${dia} de ${mes}`;
}
