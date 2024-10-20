using Microsoft.AspNetCore.Mvc;

namespace ASPConnect2MySQL.Controllers
{
    public class Product : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
