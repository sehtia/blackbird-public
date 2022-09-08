
// Income is based on company_nam and job_title
// const updateIncome = async () => {
//     try {
//         // TODO: Format url instead
//         const data = await fetch(
//             `https://gradient.pythonanywhere.com/getSherlockStakerWalletStats`
//         );
//         const json = await data.json();
//         active_wallet_percent = Math.percent(json.isActiveWalletPercent*100)/100;
//         inactive_wallet_percent = 1 - active_wallet_percent;
//         console.log(active_wallet_percent);
//     } catch (err) {
//         console.error(`Error getting income: ${err}`);
//     }
// };

export const anotherFileData = [
    {
      "name": "Active Wallets",
      "value": 50,
      "fill" : "#FF8042"
    },
    {
      "name": "Inactive Wallets",
      "value": 50,
      "fill" : "#FFBB28"
    }
  ];
